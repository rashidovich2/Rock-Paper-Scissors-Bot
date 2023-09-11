# - *- coding: utf- 8 - *-

import datetime

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from data import db
from loader import dp
from keyboards.default.users.default_key import start


db.init_db()

with open("joined.txt", "r") as all_users_file:
    all_users = {line.strip() for line in all_users_file}


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if message.chat.type != 'private':
        return
    if str(message.chat.id) not in all_users:
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        user_id = message.chat.id
        today = datetime.datetime.now()
        date = today.strftime("%Y-%m-%d")
        all_users_file = open("joined.txt", "a")
        all_users_file.write(str(message.chat.id) + "\n")
        all_users.add(str(message.chat.id))
        keyboard = types.InlineKeyboardMarkup()
        but_1 = types.InlineKeyboardButton(
            text='Выбрать чат...', switch_inline_query="new")
        keyboard.add(but_1)
        await dp.bot.send_message(message.chat.id, "👋 Привет! Нажми на кнопку, если хочешь создать новую игру.", reply_markup=keyboard)
        await dp.bot.send_message(message.chat.id, 'ᅠ', reply_markup=start)
        db.add_user(first_name, last_name, date, user_id)
    else:
        keyboard = types.InlineKeyboardMarkup()
        but_1 = types.InlineKeyboardButton(
            text='Выбрать чат...', switch_inline_query="new")
        keyboard.add(but_1)
        await dp.bot.send_message(message.chat.id, "👋 Привет! Нажми на кнопку, если хочешь создать новую игру.", reply_markup=keyboard)
        await dp.bot.send_message(message.chat.id, 'ᅠ', reply_markup=start)
