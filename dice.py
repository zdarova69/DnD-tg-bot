from openai import OpenAI
# from game_cube import dice_roll
import random
from cl import chat_gpt
import asyncio
import json

char_bonus = {
    1: -5,
    2: -4,
    3: -4,
    4: -3,
    5: -3,
    6: -2,
    7: -2,
    8: -1,
    9: -1,
    10: 0,
    11: 0,
    12: 1,
    13: 1,
    14: 2,
    15: 2,
    16: 3,
    17: 3,
    18: 4,
    19: 4,
    20: 5,
    21: 5,
    22: 6,
    23: 6,
    24: 7,
    25: 7,
    26: 8,
    27: 8,
    28: 9,
    29: 9,
    30: 10
}

async def dice_roll():
    roll = random.randint(1, 20)
    return roll

async def action(text: str, user_id):
    # Открываем файл и загружаем его содержимое в переменную stats
    with open(f'characters_{user_id}.json', 'r', encoding='utf-8') as file:
        stats = json.load(file)
    stat = await chat_gpt(f'''
Есть характеристики: strength,agility , dexterity, constitution, intelligence, charisma, wisdom
Определи, к какой характеристике относится следующий текст: {text}.
ВАЖНО: выведи только ответ в виде одного слова с маленькой буквы на английском языке. 
''', task='dice')
    print(stat)
    diff = int(await chat_gpt(f'Оцени сложность действия по шкале от 2 до 30: {text}. ВАЖНО: выведи только ответ в виде числа', task='dice'))
    dice = await dice_roll()
    print(f'{stat}: {char_bonus[stats[stat]]}+{dice} vs {diff}')
    if (char_bonus[stats[stat]] + dice >= diff and dice != 1) or dice == 20:
        print('Успех!')
        exodus = ' POSITIVE'
    elif (char_bonus[stats[stat]]+dice < diff and dice != 20) or diff == 1:
        print('Провал...')
        exodus = ' NEGATIVE'
    return exodus

# asyncio.run(action('Я - эльф лучний'))
