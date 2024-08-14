from openai import OpenAI
# import asyncio

client = OpenAI(
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
