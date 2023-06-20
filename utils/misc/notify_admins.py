import logging
from aiogram import Dispatcher
from core.config import admins
from loader import bot
from datetime import datetime


async def on_startup_notify(dp: Dispatcher):
    for admin in admins:
        try:
            await dp.bot.send_message(chat_id=int(admin), text="Бот Запущен")
        except Exception as err:
            logging.exception(err)


async def notify_new_user_add(dp: Dispatcher, user_id, full_name):
    for admin in admins:
        try:
            logging.info(f"Добавлен новый пользователь {user_id}|{full_name}")
            await dp.bot.send_message(int(admin), f"Добавлен новый пользователь в БД [{user_id}][{full_name}]",
                                      disable_notification=True)
        except Exception as err:
            logging.exception(err)


async def shutdown_bot(dp: Dispatcher):
    for admin in admins:
        try:
            await dp.bot.send_message(int(admin), "Бот выключен")
        except Exception as err:
            logging.exception(err)
