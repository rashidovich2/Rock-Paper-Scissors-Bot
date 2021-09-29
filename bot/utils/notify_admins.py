import logging

from aiogram import Dispatcher

from data.settings import ADMIN_ID


async def on_startup_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(ADMIN_ID, "<pre>Бот запущен!</pre>", parse_mode='HTML')
    except Exception as err:
        logging.exception(err)


async def off_startup_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(ADMIN_ID, "<pre>Бот прекратил работу!</pre>", parse_mode='HTML')
    except Exception as err:
        logging.exception(err)
