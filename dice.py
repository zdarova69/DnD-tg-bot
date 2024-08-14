from openai import OpenAI
# from game_cube import dice_roll
import random
from cl import client
import asyncio
import json


async def dice_roll():
    roll = random.randint(1, 20)
    return roll


async def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


async def action(text: str, user_id):
    # Открываем файл и загружаем его содержимое в переменную stats
    with open(f'characters_{user_id}.json', 'r', encoding='utf-8') as file:
        stats = json.load(file)
    stat = await chat_gpt(f'''
Есть характеристики: strength,agility , dexterity, constitution, intelligence, charisma, wisdom
Определи, к какой характеристике относится следующий текст: {text}.
ВАЖНО: выведи только ответ в виде одного слова с маленькой буквы на английском языке. 
''')
    print(stat)
    diff = int(await chat_gpt(f'Оцени сложность действия по шкале от 2 до 30: {text}. ВАЖНО: выведи только ответ в виде числа'))
    dice = await dice_roll()
    print(f'{stat}: {stats[stat]}+{dice} vs {diff}')
    if (stats[stat] + dice >= diff and dice != 1) or dice == 20:
        print('Успех!')
        exodus = ' POSITIVE'
    elif (stats[stat]+dice < diff and dice != 20) or dice == 1:
        print('Провал...')
        exodus = ' NEGATIVE'
    return exodus

# asyncio.run(action('Я - эльф лучний'))
