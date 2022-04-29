from loader import dp
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.menu_inline import start_menu_cd
import asyncio

async def get_documents(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=start_menu_cd.new(button_id="button_start"))
    )
    file_id = 'BQACAgIAAxkBAANhYmv1WkfSgHs1XRlzcI61cgLmcQcAAs4UAALYMmBLstdgd03_1o0kBA'
    await dp.bot.send_document(chat_id=call.from_user.id, document=file_id, reply_markup=markup)
    await dp.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
