import asyncio
import logging
import sys
import json

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
# from gen_message import generate_message
# from translater import ru, en
from model import save, generate

# Открываем файл в режиме чтения
with open('tg_api.txt', 'r') as file:
    # Читаем содержимое файла
    TOKEN = file.read()

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    greeting = '''
Привет, путник. Мы, два разраба, рады, что ты заскочил к нам.
Позволь нам рассказать одну историю, но сперва давай определимся с главным героем - /create_character.
А когда ты будешь готов, введи что-нибудь вроде "начать игру", и тогда мы начнем рассказ.
А что будет дальше....решать тебе.
<a href="https://github.com/zdarova69/DnD-tg-bot">(А вот наш репозиторий)</a>
    '''
    await message.answer(greeting)


class CharacterCreation(StatesGroup):
    name = State()
    race = State()
    char_class = State()
    strength = State()
    agility = State()
    dexterity = State()
    constitution = State()
    intelligence = State()
    wisdom = State()
    charisma = State()
    background = State()
    finish = State()
    


@dp.message(Command('create_character'))
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(CharacterCreation.race)
    await message.answer("Как зовут главного героя?")


@dp.message(CharacterCreation.race)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(CharacterCreation.char_class)
    await message.answer(
        f"выбери расу",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="🧝‍♂️ человек"),
                    KeyboardButton(text="🧝🏻‍♂️ эльф"),
                    KeyboardButton(text="🧝‍♀️ полуэльф"),
                    KeyboardButton(text="🧔 дворф"),
                    KeyboardButton(text="👿 тифлинг"),
                    KeyboardButton(text="🦹🏿‍♂️ дроу"),
                    KeyboardButton(text="🐉 гитьянки"),
                    KeyboardButton(text="👶 гномы"),
                    KeyboardButton(text="🧟 полуорки"),
                    KeyboardButton(text="🐲 драконорожденные"),
                ]
            ],
            resize_keyboard=True,
        ),
    )


@dp.message(CharacterCreation.char_class)
async def process_race(message: types.Message, state: FSMContext):
    await state.update_data(race=message.text)
    await state.set_state(CharacterCreation.strength)
    await message.answer(
        f"выбери класс",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="⚔️ воин"),
                    KeyboardButton(text="🪓 варвар"),
                    KeyboardButton(text="🎵 бард"),
                    KeyboardButton(text="🌿 друид"),
                    KeyboardButton(text="🧙🏻‍♀️ жрец"),
                    KeyboardButton(text="🔮 колдун"),
                    KeyboardButton(text="🧙‍♂️ волшебник"),
                    KeyboardButton(text="✨ чародей"),
                    KeyboardButton(text="🥋 монах"),
                    KeyboardButton(text="👣 следопыт"),
                    KeyboardButton(text="🗡️ плут")
                ]
            ],
            resize_keyboard=True,
        ),
    )

i = 60

@dp.message(CharacterCreation.strength)
async def process_strength(message: types.Message, state: FSMContext):
    await state.update_data(char_class=message.text)
    await state.set_state(CharacterCreation.agility)
    await message.answer(
        f"Укажи силу: максимум 18\n(осталось {i} очков)",
        reply_markup=ReplyKeyboardRemove(),

    )



@dp.message(CharacterCreation.agility)
async def process_agility(message: types.Message, state: FSMContext):
    global i  # Объявляем, что будем использовать глобальную переменную i
    try:    
        value = int(message.text)  # Преобразуем текст в целое число
        if value > 18 or value > i:      
            100 / 0
        else:
            i -= value  # Вычитаем значение из i    
            await state.update_data(agility=value)
            await state.update_data(strength=value)
            await state.update_data(i=i)
            await state.set_state(CharacterCreation.dexterity)
            await message.answer(
        f"Укажи ловкость: максимум 18\n(осталось {i} очков)",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    except (ValueError, ZeroDivisionError) as e:
        await message.reply(f"Ошибка: текст не является целым числом")
    
 


@dp.message(CharacterCreation.dexterity)
async def process_dexterity(message: types.Message, state: FSMContext):
    global i  # Объявляем, что будем использовать глобальную переменную i
    try:    
        value = int(message.text)  # Преобразуем текст в целое число
        if value > 18 or value > i:      
            100 / 0
        else:
            i -= value  # Вычитаем значение из i
            await state.update_data(agility=int(message.text))
            await state.update_data(i=i)
            await state.set_state(CharacterCreation.constitution)
            await message.reply(f"Укажи выносливость: максимум 18\n(осталось {i} очков)")   
    except (ValueError, ZeroDivisionError) as e:
        await message.reply(f"Ошибка: текст не является целым числом")
    

@dp.message(CharacterCreation.constitution)
async def process_constitution(message: types.Message, state: FSMContext):
    global i  # Объявляем, что будем использовать глобальную переменную i
    try:    
        value = int(message.text)  # Преобразуем текст в целое число
        if value > 18 or value > i:      
            100 / 0
        else:
            i -= value  # Вычитаем значение из i
            await state.update_data(agility=int(message.text))
            await state.update_data(agility=int(message.text))
            await state.update_data(dexterity=int(message.text))
            await state.update_data(i=i)
            await state.set_state(CharacterCreation.intelligence)
            await message.reply(f"Укажи живучесть: максимум 18\n(осталось {i} очков)")
    except (ValueError, ZeroDivisionError) as e:
        await message.reply(f"Ошибка: текст не является целым числом")
    


@dp.message(CharacterCreation.intelligence)
async def process_intelligence(message: types.Message, state: FSMContext):
    global i  # Объявляем, что будем использовать глобальную переменную i
    try:    
        value = int(message.text)  # Преобразуем текст в целое число
        if value > 18 or value > i:      
            100 / 0
        else:
            i -= value  # Вычитаем значение из i
            await state.update_data(agility=int(message.text))
            await state.update_data(agility=int(message.text))
            await state.update_data(constitution=int(message.text))
            await state.update_data(i=i)
            await state.set_state(CharacterCreation.charisma)
            await message.reply(f"Укажи интеллект: максимум 18\n(осталось {i} очков)")   
    except (ValueError, ZeroDivisionError) as e:
        await message.reply(f"Ошибка: текст не является целым числом")
    

@dp.message(CharacterCreation.charisma)
async def process_charisma(message: types.Message, state: FSMContext):
    global i  # Объявляем, что будем использовать глобальную переменную i
    try:    
        value = int(message.text)  # Преобразуем текст в целое число
        if value > 18 or value > i:      
            100 / 0
        else:
            i -= value  # Вычитаем значение из i
            await state.update_data(agility=int(message.text))
            await state.update_data(intelligence=int(message.text))
            await state.update_data(i=i)
            await state.set_state(CharacterCreation.wisdom)
            await message.reply(f"Укажи харизму: максимум 18\n(осталось {i} очков)")
    except (ValueError, ZeroDivisionError) as e:
        await message.reply(f"Ошибка: текст не является целым числом")
    

@dp.message(CharacterCreation.wisdom)
async def process_wisdom(message: types.Message, state: FSMContext):
    global i  # Объявляем, что будем использовать глобальную переменную i
    try:    
        value = int(message.text)  # Преобразуем текст в целое число
        if value > 18 or value > i:      
            100 / 0
        else:
            i -= value  # Вычитаем значение из i
            await state.update_data(agility=int(message.text))
            await state.update_data(charisma=int(message.text))
            await state.update_data(i=i)
            await state.set_state(CharacterCreation.background)
            await message.reply(f"Укажи мудрость: максимум 18\n(осталось {i} очков)")
    except (ValueError, ZeroDivisionError) as e:
        await message.reply(f"Ошибка: текст не является целым числом")


@dp.message(CharacterCreation.background)
async def process_background(message: types.Message, state: FSMContext):
    await state.update_data(wisdom=int(message.text))
    await state.set_state(CharacterCreation.finish)
    await message.reply("А теперь подумай, какая у твоего героя была предыстория, и напиши её сюда.")

    

@dp.message(CharacterCreation.finish)
async def complete_customization(message: types.Message, state: FSMContext):
    await state.update_data(background=message.text)
    data = await state.get_data()
    user_id = message.from_user.id
    character = {
        'name': data['name'],
        'race': data['race'],
        'class': data['char_class'],
        'strength': data['strength'],
        'agility': data['agility'],
        'dexterity': data['dexterity'],
        'constitution': data['constitution'],
        'intelligence': data['intelligence'],
        'charisma': data['charisma'],
        'wisdom': data['wisdom']
    }

    with open(f'characters_{user_id}.json', 'w', encoding='utf-8') as f:
        json.dump(character, f, ensure_ascii=False)

    await message.reply("Подождите...")
    current_state = await state.get_state()
    await message.reply(f'''
Персонаж создан и сохранен!
Имя - {data['name']},
Раса - {data['race']},
Класс - {data['char_class']},
Сила - {data['strength']},
Ловкость - {data['agility']},
Выносливость - {data['dexterity']},
Живучесть - {data['constitution']},
Интеллект - {data['intelligence']},
Харизма - {data['charisma']},
Мудрость - {data['wisdom']},
<b>Предыстория</b>:
<i>{data['background']}</i>
    ''')
    await message.reply(await generate(f'''
    Запомни, вот главный герой:
    Имя - {data['name']}
    Раса - {data['race']}
    Класс - {data['char_class']}
    Предыстория:
    {data['background']}
        ''', user_id=user_id))
    if current_state is None:
        return
    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await save(message.text)
        await message.reply(await generate(message.text, user_id=message.from_user.id))
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
