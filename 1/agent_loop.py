import json, sys, json, uuid, time
from pathlib import Path
from copy import deepcopy

from tools.tools import get_weather, calculator 
from tools.registry import TOOL_REGISTRY
from tools.utils import run_tool, get_schema
from llm.LLM import client
from data.dataclass import AgentResult, ToolCallRecord
from conversation.conversation import Conversation, MAX_TOOL_OUTPUT_CHARS
from trace_utils import Trace

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")



def run_agent(conv: Conversation, t: Trace, max_steps: int=3):

    tools = get_schema()
    tool_calls: list[ToolCallRecord] = []
    t.gen_trace_id()

    for step in range(max_steps):
        
        t0 = time.perf_counter()
        stream = client.responses.create(
            model="deepseek-v4-flash",
            tools=tools,
            instructions=conv.instructions,
            input=conv.items,
            stream=True
        )
        response = None
        for event in stream:
            if event.type == "response.output_text.delta":
                time.sleep(0.05)
                print(event.delta, end="", flush=True)
            elif event.type == "response.completed":
                response = event.response

        t.insert_llm_call(response=response, conv=conv, step=step, t0=t0)
        conv.add_response_output(response_output=response.output)
        usage = response.usage.model_dump() if getattr(response, "usage", None) else {}
        
        if not any(it for it in response.output if it.type == "function_call"):
            
            t.save()
            return AgentResult(
                final_text=response.output_text,
                status="completed",
                steps=step+1,
                tool_calls=tool_calls,
                usage=usage                
            )
             
        for item in response.output:
            if item.type == "function_call":
                t1 = time.perf_counter()
                result, err = run_tool(item.name, item.arguments)
                result = result[:MAX_TOOL_OUTPUT_CHARS]
                tool_calls.append(ToolCallRecord(item.name, item.arguments, result, err))
                conv.add_tool_output(item.call_id, result)
                t.insert_tool_call(item=item, result=result, step=step, err=err, t1=t1)

        conv.trim()
    t.save()
    return AgentResult(
        final_text="",
        status="incompleted",
        steps=max_steps,
        tool_calls=tool_calls,
        usage=usage
    )
                              

if __name__ == "__main__":
    
    t = Trace()
    conv = Conversation("你是个AI助手，优先使用工具获取数据")
    conv.add_user("今天天津的天气如何，顺便帮我计算一下123乘以456等于多少")
    agent_result = run_agent(conv, t)
    # print("状态：", agent_result.status, "|步数：", agent_result.steps, "|消耗tokens：", agent_result.usage)
    # print("\n最终答案：", agent_result.final_text)
    print("\n")
    conv.add_user("刚才那条天气再帮我确认一下")
    agent_result1 = run_agent(conv, t)
    # print(agent_result1.final_text)

    


