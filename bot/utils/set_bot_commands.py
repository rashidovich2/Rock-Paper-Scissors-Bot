from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Начать игру"),
            types.BotCommand("stats", "Моя статистика"),
            types.BotCommand("help", "Помощь")
        ]
    )
