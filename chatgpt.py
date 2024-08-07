import os
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key=, 
    base_url="https://api.proxyapi.ru/openai/v1",
)

chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello world"}]
)