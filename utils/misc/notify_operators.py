import logging

from aiogram import Dispatcher

from core.config import operators, admins
from keyboards.support_keyborad import notify_operators_markup


async def notify_new_question(dp: Dispatcher):
    for operator in operators:
        try:
            logging.info("Пришел новый вопрос")
            await dp.bot.send_message(int(operator), "Пришел новый вопрос", reply_markup=notify_operators_markup(operator))
        except Exception as err:
            logging.exception(err)
    for admin in admins:
        try:
            logging.info("Пришел новый вопрос")
            await dp.bot.send_message(int(admin), "Пришел новый вопрос", reply_markup=notify_operators_markup(admin), disable_notification=True)
        except Exception as err:
            logging.exception(err)


