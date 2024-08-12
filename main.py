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
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
# from gen_message import generate_message
from translater import ru, en
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
    greeting = '''Привет, я DnD бот. могу придумать тебе историю'''
    await message.answer(greeting)

class CharacterCreation(StatesGroup):
    name = State()
    race = State()
    char_class = State()
    strength = State()
    dexterity = State()
    constitution = State()
    intelligence = State()
    wisdom = State()

@dp.message(Command('create_characters'))
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(CharacterCreation.name)
    await message.answer(
        "Давай придумаем имя персонажа",
    )
# @dp.message(Command("cancel"))
# @dp.message(F.text.casefold() == "cancel")

# async def cancel_handler(message: Message, state: FSMContext) -> None:
#     """
#     Allow user to cancel any action
#     """
#     current_state = await state.get_state()
#     if current_state is None:
#        return
#     logging.info("Cancelling state %r", current_state)
#     await state.clear()
#     await message.answer(
#         "Cancelled.",
#     )
@dp.message(CharacterCreation.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(CharacterCreation.race)
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

@dp.message(CharacterCreation.race)
async def process_race(message: types.Message, state: FSMContext):
    await state.update_data(race=message.text)
    await state.set_state(CharacterCreation.char_class)
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


@dp.message(CharacterCreation.char_class)
async def process_class(message: types.Message, state: FSMContext):
    await state.update_data(char_class=message.text)
    await state.set_state(CharacterCreation.strength)
    await message.answer(
        "Укажи силу:",
        reply_markup=ReplyKeyboardRemove(),

    )


@dp.message(CharacterCreation.strength)
async def process_strength(message: types.Message, state: FSMContext):
    await state.update_data(strength=int(message.text))
    await state.set_state(CharacterCreation.dexterity)
    await message.answer(
        "Укажи ловкость:",
        reply_markup=ReplyKeyboardRemove(),

    )
    

@dp.message(CharacterCreation.dexterity)
async def process_dexterity(message: types.Message, state: FSMContext):
    await state.update_data(dexterity=int(message.text))
    await state.set_state(CharacterCreation.constitution)
    await message.reply("Укажи выносливость:")
    

@dp.message(CharacterCreation.constitution)
async def process_constitution(message: types.Message, state: FSMContext):
    await state.update_data(constitution=int(message.text))
    await state.set_state(CharacterCreation.intelligence)
    await message.reply("Укажи интеллект:")
    

@dp.message(CharacterCreation.intelligence)
async def process_intelligence(message: types.Message, state: FSMContext):
    await state.update_data(intelligence=int(message.text))
    await state.set_state(CharacterCreation.wisdom)
    await message.reply("Укажи мудрость:")
    

@dp.message(CharacterCreation.wisdom)
async def process_wisdom(message: types.Message, state: FSMContext):
    await state.update_data(wisdom=int(message.text))
    await state.set_state(CharacterCreation.wisdom)

    data = await state.get_data()
    user_id = message.from_user.id
    character = {
        'name': data['name'],
        'race': data['race'],
        'class': data['char_class'],
        'strength': data['strength'],
        'dexterity': data['dexterity'],
        'constitution': data['constitution'],
        'intelligence': data['intelligence'],
        'wisdom': data['wisdom']
    }

    with open(f'characters_{user_id}.json', 'w', encoding='utf-8') as f:
        json.dump(character, f, ensure_ascii=False)

    await message.reply("Персонаж создан и сохранен!")
    await state.finish()

@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await save(message.text)
        await message.reply(await generate(message.text))
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