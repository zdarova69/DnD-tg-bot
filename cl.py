from openai import OpenAI
# import asyncio

client = OpenAI(
    # This is the default and can be omitted
    api_key='sk-579fKdJoDNX5nxitko27C0e3BHjCwKfG', 
    base_url="https://api.proxyapi.ru/openai/v1",
    )

async def chat_gpt(prompt, task):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    if task == 'dice':
        result = response.choices[0].message.content.strip()
    if task == 'img':
        result = response.choices[0].message.content
 
    return result
    
# asyncio.run(chat_gpt('в траве сидел кузнечик', 'img'))