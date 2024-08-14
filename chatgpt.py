import os
from openai import OpenAI
import random
from dice import action
from cl import client



async def generate_message(prompt, user_id):
    exodus = await action(prompt, user_id)
    prompt = prompt + exodus
    print(prompt)
    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini", 
        messages=[
            {"role": "system", "content": "Ты - гейм-мастер игры по Dungeon and Dragons. ты можешь иногда получать в сообщении POSITIVE или NEGATIVE - это будет означать, что ты должен будешь создать позитивное или негативное продолжение событий"},
            {"role": "user", "content": prompt},
        ]
    )
    print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content



async def generate_image(prompt):
    response = client.images.generate(
        model="dall-e-2",
        prompt=prompt,
        # style='vivid',
        n=1,
        size="512x512"

)
    return response.data[0].url

# print(generate_message('я читаю заклинание чтобы поднять камень'))
# print(generate_image('эльф лучник сидит в лесу на дереве'))


