from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY") 
#客户端
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)