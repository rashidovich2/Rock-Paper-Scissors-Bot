# - *- coding: utf- 8 - *-

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


moves = types.InlineKeyboardMarkup()
but_1 = types.InlineKeyboardButton(
    text='✊', callback_data="Rock")
but_2 = types.InlineKeyboardButton(
    text='✌️', callback_data="Scissors")
but_3 = types.InlineKeyboardButton(
    text='✋', callback_data="Paper")
moves.add(but_1, but_2, but_3)
