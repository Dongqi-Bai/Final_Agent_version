
from dataclasses import dataclass, field


MAX_TOOL_OUTPUT_CHARS = 2000
MAX_HISTORY_ITMES = 20

@dataclass
class Conversation:
    
    instructions: str
    items: list[dict] = field(default_factory=list)
        
    def add_user(self, message: str):
        self.items.append({"role":"user","content":message})
    
    def add_response_output(self, response_output):
        self.items.extend(self._clean(out.model_dump()) for out in response_output)
        
    def add_tool_output(self, call_id: str, output):
        self.items.append(
            {
                "type":"function_call_output",
                "call_id":call_id,
                "output":output
            }
        )
        
    @staticmethod
    def _clean(d: dict):
        if d.get("type") == "function_call":
            return {
                "type":"function_call",
                "call_id":d["call_id"],
                "name":d["name"],
                "arguments":d.get("arguments", "{}")
            }
        if d.get("type") == "message":
            return {
                "role":"assistant",
                "content":d.get("content", [])
            }
        return d
        
    def trim(self):
        if len(self.items) > MAX_HISTORY_ITMES:
            n = len(self.items) - MAX_HISTORY_ITMES
            self.items = self.items[n:]
            
            
            