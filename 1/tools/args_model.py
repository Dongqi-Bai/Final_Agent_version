

from pydantic import BaseModel, Field


class CalculatorArgs(BaseModel):
    a: float = Field(description="第一个乘数")
    b: float = Field(description="第二个乘数")
    
class WeatherArgs(BaseModel):
    city: str = Field(description="一个城市名称，如北京，上海")
    
    