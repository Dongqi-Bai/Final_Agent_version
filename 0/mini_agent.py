import json
import sys

from openai import OpenAI
from dotenv import load_dotenv
import os

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY") 
#客户端
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

#天气工具
def get_weather(city: str)->str:
    return f"{city}，今天晴，温度26度"

def calculator(a, b):
    return a*b
    
tools = [
    {
        "type":"function",
        "name":"calculator",
        "description":"计算数学表达式",
        "parameters":{
            "type":"object",
            "properties":{
                "a":{
                    "type":"number",
                    "description":"第一个乘数"
                },
                "b":{
                    "type":"number",
                    "description":"第二个乘数"
                }
            },
            "required":["a", "b"]
        }
    },
    {
        "type":"function",
        "name":"get_weather",
        "description":"查询某城市的天气",
        "parameters":{
            "type":"object",
            "properties":{
                "city":{
                    "type":"string",
                    "description":"一个城市的名称，如北京、上海"
                }
            },
            "required":["city"]
        }
    }
]

def run_agent(messages: str, max_steps: int=3):
    messages = [{"role":"user","content":messages}]
    instructions = "你是个AI助手，优先使用工具获取数据"

    for step in range(max_steps):
        response = client.responses.create(
            model="deepseek-v4-flash",
            tools=tools,
            instructions=instructions,
            input=messages
        ) 
        for out in response.output:
            d = out.model_dump()
            messages.append(d)

        
        call = [it for it in response.output if it.type == "function_call"]
        if not call:
            print("step:",step)
            #print(response.model_dump_json())
            print(response.output_text)
            break

        for item in response.output:
            if item.type == "function_call":
                try:
                    if item.name == "get_weather":
                        city = json.loads(item.arguments)["city"]
                        result = get_weather(city)

                    elif item.name == "calculator":
                        args = json.loads(item.arguments)
                        a = args["a"]
                        b = args["b"]
                        result = str(calculator(a, b))
        
                    else:
                        result = f"未知工具，{item.name}"
                    messages.append(
                        {
                            "type":"function_call_output",
                            "call_id":item.call_id,
                            "output":result
                        }
                    )
                except Exception as e:
                    result = f"工具执行出错，{e}"
                    messages.append(
                        {
                            "type":"function_call_output",
                            "call_id":item.call_id,
                            "output":result
                        }
                    )

    return "达到最大调用次数"
                
                

if __name__ == "__main__":
    run_agent("今天天津的天气如何，顺便帮我计算一下123乘以456等于多少")
    


