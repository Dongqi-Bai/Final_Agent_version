from copy import deepcopy
from dataclasses import dataclass, field
import json
from pathlib import Path
import time
import uuid


@dataclass
class Trace:
    
    trace_logs :list[dict] = field(default_factory=list)
    TRACE_DIR = Path(__file__).resolve().parent / "traces"
    trace_id: str = field(default_factory=str)
    
    def gen_trace_id(self):
        self.trace_id = uuid.uuid4().hex[:12]
    
    def insert_llm_call(self,response, conv, step, t0):
    
        self.trace_logs.append(
            {
                "type":"llm_call",
                "trace_id":self.trace_id,
                "response_id":response.id,
                "step":step,
                "input":deepcopy(conv.items),
                "output":response.model_dump(),
                "usage":response.usage.model_dump(),
                "latency_ms": round((time.perf_counter() - t0) * 1000, 1)
            }
        )
        
    def insert_tool_call(self, item, result, step, err, t1):
        
        self.trace_logs.append(
            {
                "type":"tool_call",
                "trace_id":self.trace_id,
                "step":step,
                "name":item.name,
                "arguments":item.arguments,
                "result":result,
                "err":err,
                "latency_ms": round((time.perf_counter() - t1) * 1000, 1)
            }
        )
    
    def save(self):
        
        self.TRACE_DIR.mkdir(exist_ok=True, parents=True)
        
        (self.TRACE_DIR / f"{self.trace_id}.jsonl").write_text(
        "\n".join(json.dumps(e, ensure_ascii=False, default=str) for e in self.trace_logs), encoding="utf-8")
    
    
    
    