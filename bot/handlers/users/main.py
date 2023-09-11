# - *- coding: utf- 8 - *-

import random
import hashlib
import datetime
from time import sleep

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineQuery, \
    InputTextMessageContent, InlineQueryResultArticle

from data import db
from loader import dp
from keyboards.inline.users.inline_key import moves


with open("joined.txt", "r") as all_users_file:
    all_users = {line.strip() for line in all_users_file}


@dp.message_handler(commands=["stats"])
async def stat_command(message: types.Message):
    try:
        wins = int(db.return_user_wins_2(message.chat.id))
        games = int(db.return_user_games(message.chat.id))
        losses = games - wins
        keyboard = types.InlineKeyboardMarkup()
        but_1 = types.InlineKeyboardButton(
            text='Поделиться статистикой', switch_inline_query="share_stats")
        keyboard.add(but_1)
        if wins == 0:
            await dp.bot.send_message(message.chat.id, f"✔️ {games}\n🏆 0 (0%)\n🚫 {losses}", reply_markup=keyboard)
        else:
            procent_wins = (wins / games) * 100
            await dp.bot.send_message(message.chat.id, f"✔️ {games}\n🏆 {wins} ({round(procent_wins)}%)\n🚫 {losses}", reply_markup=keyboard)
    except:
        pass


@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await dp.bot.send_message(message.chat.id, 'Разработчик: @por0vos1k\n\nПроект на Github - <a href="https://github.com/famaxth/Rock-Paper-Scissors-Bot">ссылка</a>', parse_mode='HTML')


@dp.message_handler()
async def main(message):
    if message.chat.type != 'private':
        return
    if message.text == "Помощь":
        await dp.bot.send_message(message.chat.id, 'Разработчик: @por0vos1k\n\nПроект на Github - <a href="https://github.com/famaxth/Rock-Paper-Scissors-Bot">ссылка</a>', parse_mode='HTML')
    elif message.text == "Моя статистика":
        try:
            wins = int(db.return_user_wins_2(message.chat.id))
            games = int(db.return_user_games(message.chat.id))
            losses = games - wins
            keyboard = types.InlineKeyboardMarkup()
            but_1 = types.InlineKeyboardButton(
                text='Поделиться статистикой', switch_inline_query="share_stats")
            keyboard.add(but_1)
            if wins == 0:
                await dp.bot.send_message(message.chat.id, f"✔️ {games}\n🏆 0 (0%)\n🚫 {losses}", reply_markup=keyboard)
            else:
                procent_wins = (wins / games) * 100
                await dp.bot.send_message(message.chat.id, f"✔️ {games}\n🏆 {wins} ({round(procent_wins)}%)\n🚫 {losses}", reply_markup=keyboard)
        except:
            pass
    else:
        keyboard = types.InlineKeyboardMarkup()
        but_1 = types.InlineKeyboardButton(
            text='Выбрать чат...', switch_inline_query="new")
        keyboard.add(but_1)
        await dp.bot.send_message(message.chat.id, "👋 Привет! Нажми на кнопку, если хочешь создать новую игру.", reply_markup=keyboard)


@dp.inline_handler()
async def inline_echo(inline_query: InlineQuery):
    wins = int(db.return_user_wins_2(inline_query.from_user.id))
    games = int(db.return_user_games(inline_query.from_user.id))
    losses = games - wins
    keyboard = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(
        text='Поделиться статистикой', switch_inline_query="share_stats")
    keyboard.add(but_1)
    if wins == 0:
        input_content_2 = f"Моя статистика:\n✔️ {games}\n🏆 0 (0%)\n🚫 {losses}\n\nА сколько выигрышей у тебя?"
    else:
        procent_wins = (wins / games) * 100
        input_content_2 = f"Моя статистика:\n✔️ {games}\n🏆 {wins} ({round(procent_wins)}%)\n🚫 {losses}\n\nА сколько выигрышей у тебя?"
    text = 'Новая игра'
    input_content = InputTextMessageContent('Камень, ножницы, бумага:')
    input_content_2 = InputTextMessageContent(input_content_2)
    item_1 = InlineQueryResultArticle(
        id='1',
        title=text,
        description='Камень-Ножницы-Бумага',
        input_message_content=input_content,
        reply_markup=moves,
    )
    item_2 = InlineQueryResultArticle(
        id='2',
        title='Поделиться статистикой',
        input_message_content=input_content_2,
        reply_markup=keyboard,
    )
    await dp.bot.answer_inline_query(inline_query.id, results=[item_1, item_2])


@dp.callback_query_handler(lambda c: c.data, state=None)
async def inline(call: types.CallbackQuery, state: FSMContext):
    if not str(call.from_user.id) in all_users:
        first_name = call.from_user.first_name
        last_name = call.from_user.last_name
        user_id = call.from_user.id
        today = datetime.datetime.today()
        date = today.strftime("%Y-%m-%d")
        all_users_file = open("joined.txt", "a")
        all_users_file.write(str(call.from_user.id) + "\n")
        all_users.add(str(call.from_user.id))
        db.add_user(first_name, last_name, date, user_id)
        text = call.data[-1]
        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        if text not in numbers:
            name = str(call.from_user.first_name)
            if call.from_user.last_name != None:
                name = name + " " + str(call.from_user.last_name)
            else:
                pass
            db.add_game(call.data, name, call.from_user.id)
            game = db.return_game_number()
            keyboard = types.InlineKeyboardMarkup()
            but_1 = types.InlineKeyboardButton(
                text='✊', callback_data=f"Rock{game}")
            but_2 = types.InlineKeyboardButton(
                text='✌️', callback_data=f"Scissors{game}")
            but_3 = types.InlineKeyboardButton(
                text='✋', callback_data=f"Paper{game}")
            keyboard.add(but_1, but_2, but_3)
            await dp.bot.edit_message_text(inline_message_id=call.inline_message_id, text="Камень, ножницы, бумага:\nЯ сделал ход\nожидание противника...", reply_markup=keyboard)
        else:
            result = db.return_info_game(int(text))
            if result != None:
                if call.from_user.id != result[3]:
                    player_2_name = str(call.from_user.first_name)
                    if call.from_user.last_name != None:
                        player_2_name = player_2_name + " " + \
                            str(call.from_user.last_name)
                    player_1_name = result[2]
                    move_1 = result[1]
                    move_2 = call.data[0:-1]
                    try:
                        if move_1 == "Rock":
                            move_1 = "✊"
                        elif move_1 == "Paper":
                            move_1 = "✋"
                        elif move_1 == "Scissors":
                            move_1 = "✌️"
                    except:
                        pass
                    try:
                        if move_2 == "Rock":
                            move_2 = "✊"
                        elif move_2 == "Paper":
                            move_2 = "✋"
                        elif move_2 == "Scissors":
                            move_2 = "✌️"
                    except:
                        pass
                    if move_1 == move_2:
                        keyboard = types.InlineKeyboardMarkup()
                        but_1 = types.InlineKeyboardButton(
                            text='Новая игра | New game', switch_inline_query="new")
                        keyboard.add(but_1)
                        await dp.bot.edit_message_text(inline_message_id=call.inline_message_id, text=f"<a>{player_1_name}  {move_1} <b>VS</b> {player_2_name} {move_2}\n<b>🏳️ Ничья</b>\n\n<a href='t.me/por0vos1k'>👻 Разработчик</a></a>", disable_web_page_preview=True, reply_markup=keyboard)
                        db.delete_game(int(text))
                        all_games = db.return_user_games(call.from_user.id)
                        all_games_2 = db.return_user_games(result[3])
                        db.update_user_stat_loss(call.from_user.id, all_games)
                        db.update_user_stat_loss(result[3], all_games_2)
                    elif move_1 == "✊" and move_2 == "✋":
                        winner = player_2_name
                        winner_id = call.from_user.id
                    elif move_1 == "✋" and move_2 == "✊":
                        winner = player_1_name
                        winner_id = result[3]
                    elif move_1 == "✋" and move_2 == "✌️":
                        winner = player_2_name
                        winner_id = call.from_user.id
                    elif move_1 == "✌️" and move_2 == "✋":
                        winner = player_1_name
                        winner_id = result[3]
                    elif move_1 == "✊" and move_2 == "✌️":
                        winner = player_1_name
                        winner_id = result[3]
                    elif move_1 == "✌️" and move_2 == "✊":
                        winner = player_2_name
                        winner_id = call.from_user.id
                    if move_1 != move_2:
                        if move_1 == "✊" and move_2 == "✋":
                            winner = player_2_name
                            winner_id = call.from_user.id
                        elif move_1 == "✋" and move_2 == "✊":
                            winner = player_1_name
                            winner_id = result[3]
                        elif move_1 == "✋" and move_2 == "✌️":
                            winner = player_2_name
                            winner_id = call.from_user.id
                        elif move_1 == "✌️" and move_2 == "✋":
                            winner = player_1_name
                            winner_id = result[3]
                        elif move_1 == "✊" and move_2 == "✌️":
                            winner = player_1_name
                            winner_id = result[3]
                        elif move_1 == "✌️" and move_2 == "✊":
                            winner = player_2_name
                            winner_id = call.from_user.id
                        keyboard = types.InlineKeyboardMarkup()
                        but_1 = types.InlineKeyboardButton(
                            text='Новая игра | New game', switch_inline_query="new")
                        keyboard.add(but_1)
                        await dp.bot.edit_message_text(inline_message_id=call.inline_message_id, text=f"<a>{player_1_name}  {move_1} <b>VS</b> {player_2_name} {move_2}\n<b>🏆 {winner}</b>\n\n<a href='t.me/por0vos1k'>👻 Разработчик</a></a>", disable_web_page_preview=True, reply_markup=keyboard)
                        db.delete_game(int(text))
                        wins = db.return_user_wins(winner_id)
                        all_games = db.return_user_games(winner_id)
                        all_games_2 = db.return_user_games(result[3])
                        db.update_user_stat_victory(winner_id, wins, all_games)
                        db.update_user_stat_loss(
                            call.from_user.id, all_games_2)
    else:
        text = call.data[-1]
        numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        if text not in numbers:
            name = str(call.from_user.first_name)
            if call.from_user.last_name != None:
                name = name + " " + str(call.from_user.last_name)
            else:
                pass
            db.add_game(call.data, name, call.from_user.id)
            game = db.return_game_number()
            keyboard = types.InlineKeyboardMarkup()
            but_1 = types.InlineKeyboardButton(
                text='✊', callback_data=f"Rock{game}")
            but_2 = types.InlineKeyboardButton(
                text='✌️', callback_data=f"Scissors{game}")
            but_3 = types.InlineKeyboardButton(
                text='✋', callback_data=f"Paper{game}")
            keyboard.add(but_1, but_2, but_3)
            await dp.bot.edit_message_text(inline_message_id=call.inline_message_id, text="Камень, ножницы, бумага:\nЯ сделал ход\nожидание противника...", reply_markup=keyboard)
        else:
            result = db.return_info_game(int(text))
            if result != None:
                if call.from_user.id != result[3]:
                    player_2_name = str(call.from_user.first_name)
                    if call.from_user.last_name != None:
                        player_2_name = player_2_name + " " + \
                            str(call.from_user.last_name)
                    player_1_name = result[2]
                    move_1 = result[1]
                    move_2 = call.data[0:-1]
                    try:
                        if move_1 == "Rock":
                            move_1 = "✊"
                        elif move_1 == "Paper":
                            move_1 = "✋"
                        elif move_1 == "Scissors":
                            move_1 = "✌️"
                    except:
                        pass
                    try:
                        if move_2 == "Rock":
                            move_2 = "✊"
                        elif move_2 == "Paper":
                            move_2 = "✋"
                        elif move_2 == "Scissors":
                            move_2 = "✌️"
                    except:
                        pass
                    if move_1 == move_2:
                        keyboard = types.InlineKeyboardMarkup()
                        but_1 = types.InlineKeyboardButton(
                            text='Новая игра | New game', switch_inline_query="new")
                        keyboard.add(but_1)
                        await dp.bot.edit_message_text(inline_message_id=call.inline_message_id, text=f"<a>{player_1_name}  {move_1} <b>VS</b> {player_2_name} {move_2}\n<b>🏳️ Ничья</b>\n\n<a href='t.me/por0vos1k'>👻 Разработчик</a></a>", disable_web_page_preview=True, reply_markup=keyboard)
                        db.delete_game(int(text))
                        all_games = db.return_user_games(call.from_user.id)
                        all_games_2 = db.return_user_games(result[3])
                        db.update_user_stat_loss(call.from_user.id, all_games)
                        db.update_user_stat_loss(result[3], all_games_2)
                    if move_1 != move_2:
                        if move_1 == "✊" and move_2 == "✋":
                            winner = player_2_name
                            winner_id = call.from_user.id
                        elif move_1 == "✋" and move_2 == "✊":
                            winner = player_1_name
                            winner_id = result[3]
                        elif move_1 == "✋" and move_2 == "✌️":
                            winner = player_2_name
                            winner_id = call.from_user.id
                        elif move_1 == "✌️" and move_2 == "✋":
                            winner = player_1_name
                            winner_id = result[3]
                        elif move_1 == "✊" and move_2 == "✌️":
                            winner = player_1_name
                            winner_id = result[3]
                        elif move_1 == "✌️" and move_2 == "✊":
                            winner = player_2_name
                            winner_id = call.from_user.id
                        keyboard = types.InlineKeyboardMarkup()
                        but_1 = types.InlineKeyboardButton(
                            text='Новая игра | New game', switch_inline_query="new")
                        keyboard.add(but_1)
                        await dp.bot.edit_message_text(inline_message_id=call.inline_message_id, text=f"<a>{player_1_name}  {move_1} <b>VS</b> {player_2_name} {move_2}\n<b>🏆 {winner}</b>\n\n<a href='t.me/por0vos1k'>👻 Разработчик</a></a>", disable_web_page_preview=True, reply_markup=keyboard)
                        db.delete_game(int(text))
                        wins = db.return_user_wins(winner_id)
                        all_games = db.return_user_games(winner_id)
                        all_games_2 = db.return_user_games(result[3])
                        db.update_user_stat_victory(winner_id, wins, all_games)
                        db.update_user_stat_loss(
                            call.from_user.id, all_games_2)
