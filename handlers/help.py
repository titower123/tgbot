from loader import dp
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from datetime import datetime


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    print(f'|{datetime.now().strftime("%d/%m/%Y - %H:%M:%S")}|{message.from_user.id},'
          f' {message.from_user.full_name} - смотрит справку')
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку по командам",
            )

    await message.answer("\n".join(text))
