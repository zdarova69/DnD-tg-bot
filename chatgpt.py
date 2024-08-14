import os
from openai import OpenAI
import random
from dice import action
from cl import client, chat_gpt
# import asyncio


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
    text = await chat_gpt(f'''Ты — помощник, специализирующийся на создании промптов для генерации изображений на основе текстовых описаний. Твоя задача — преобразовать предоставленный текст в промпт, который будет использоваться для создания визуального контента.

Шаги для выполнения задачи:
1. Прочитай и проанализируй предоставленный текст.
2. Определи ключевые элементы и детали, которые должны быть отражены на изображении.
3. Сформулируй промпт, включающий эти ключевые элементы и детали, с указанием на необходимые визуальные аспекты.
4. Убедись, что промпт четкий и понятный для использования в генерации изображений.
текст - {prompt}''', task='img')
    print(f'промпт - {text}')
    response = client.images.generate(
        model="dall-e-2",
        prompt=text,
        n=1,
        size="512x512"

)
    return response.data[0].url
# asyncio.run(generate_message('я читаю заклинание чтобы поднять камень'))

# asyncio.run(generate_image('эльф лучник сидит в лесу на дереве'))


