from dataclasses import dataclass,field
from enum import Enum

class Status(str, Enum):
    COMPLETED = "completed"
    INCOMPLETED = "incompleted"
    
@dataclass
class ToolCallRecord:
    name: str #工具名
    arguments: str #参数列表
    output: str #执行结果
    error: bool #是否报错
    
@dataclass
class AgentResult:
    final_text: str
    status: Status = Status.COMPLETED
    steps: int = 0
    tool_calls: list[ToolCallRecord] = field(default_factory=list)
    usage: dict = field(default_factory=dict) 
    
