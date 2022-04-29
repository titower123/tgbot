import logging

from aiogram import Dispatcher

from data.config import ADMINS


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(chat_id=int(admin), text="Бот Запущен")

        except Exception as err:
            logging.exception(err)


async def notyfi_new_user_add(dp: Dispatcher, user_id, full_name):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(int(admin), f"Добавлен новый пользователь в БД [{user_id}][{full_name}]")
        except Exception as err:
            logging.exception(err)

async def shutdown_bot(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(int(admin), "Бот выключен")
        
        except Exception as err:
            logging.exception(err)