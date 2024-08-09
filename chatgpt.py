from openai import OpenAI
from game_cube import dice_roll

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    base_url='https://api.openai.com/v1',
    api_key=open('openai_token').readline(),
)


def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


stats = {
    'сила': 10,
    'выносливость': 0,
    'интеллект': 0,
    'мудрость': 10,
    'харизма': 20,
}


def action(text):
    stat = chat_gpt(f'''
Есть характеристики: сила, выносливость, интеллект, мудрость и харизма. 
Определи, к какой характеристике относится следующий текст: {text}.
ВАЖНО: выведи только ответ в виде одного слова с маленькой буквы.
''')
    dice = dice_roll()
    print(stat, stats[stat], dice)
    if stats[stat] >= dice:
        print('Успех!')
        print(chat_gpt(f'Придумай хороший исход для этого события {text}'))
    else:
        print('Провал...')
        print(chat_gpt(f'Придумай плохой исход для этого события {text}'))
    return


action(input('Ваше действие:'))
