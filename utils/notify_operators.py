import logging

from aiogram import Dispatcher

from data.config import OPERATORS_IDS
from keyboards.support_keyborad import notify_operators_markup


async def notify_new_question(dp: Dispatcher):
    for operator in OPERATORS_IDS:
        try:
            await dp.bot.send_message(int(operator), "Пришел новый вопрос" ,reply_markup=notify_operators_markup())
        except Exception as err:
            logging.exception(err)


