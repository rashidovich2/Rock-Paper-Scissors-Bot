# - *- coding: utf- 8 - *-

from aiogram import types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


start = ReplyKeyboardMarkup(resize_keyboard=True)
but_1 = KeyboardButton('Играть')
but_2 = KeyboardButton('Моя статистика')
but_3 = KeyboardButton('Помощь')
start.add(but_1)
start.add(but_2, but_3)
