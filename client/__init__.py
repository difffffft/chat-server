from openai import OpenAI
from config import CONFIG

# 客户端
base_client = OpenAI(api_key=CONFIG['APP']['OPENAI']['API_KEY'],
                     base_url=CONFIG['APP']['OPENAI']['BASE_URL'])

# 只能使用的模型
base_model = "gpt-3.5-turbo"

# 基础的响应体
base_response_headers = {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'X-Accel-Buffering': 'no',
}


# 获得系统消息
def get_base_system_messages():
    return [
        {
            "role": "system",
            "content": "You're a chat assistant!"
        }
    ]
