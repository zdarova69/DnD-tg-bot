from openai import OpenAI
# from game_cube import dice_roll
import random
from cl import client
async def dice_roll():
    roll = random.randint(1, 20)
    return roll

stats = {
    'сила': 10,
    'выносливость': 0,
    'интеллект': 0,
    'мудрость': 10,
    'харизма': 20,
}


async def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

async def action(text):
    stat = await chat_gpt(f'''
Есть характеристики: сила, выносливость, интеллект, мудрость и харизма. 
Определи, к какой характеристике относится следующий текст: {text}.
ВАЖНО: выведи только ответ в виде одного слова с маленькой буквы. 
''')
    diff = int(await chat_gpt(f'Оцени сложность действия по шкале от 2 до 30: {text}. ВАЖНО: выведи только ответ в виде числа'))
    dice = await dice_roll()
    print(f'{stat}: {stats[stat]}+{dice} vs {diff}')
    if (stats[stat] + dice >= diff and dice != 1) or dice == 20:
        print('Успех!')
        exodus = ' POSITIVE'
    elif (stats[stat]+dice < diff and dice != 20) or diff == 1:
        print('Провал...')
        exodus = ' NEGATIVE'
    return exodus

# print(action('Я - эльф лучний'))
