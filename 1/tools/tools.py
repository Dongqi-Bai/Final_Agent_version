from tools.registry import tool
from tools.args_model import *

@tool("get_weather","查询某个城市天气",WeatherArgs)
def get_weather(city: str)->str:
    return f"{city}，今天晴，温度26度"

@tool("calculator","计算两个数的乘积",CalculatorArgs)
def calculator(a, b)->str:
    return str(a*b)