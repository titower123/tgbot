from keyboards.start_keyboard import home_markup
from loader import dp
from aiogram import types
from core.config import FILE_ID

async def get_documents(call: types.CallbackQuery):
    await dp.bot.send_document(chat_id=call.from_user.id, document=FILE_ID, reply_markup=home_markup())
    await dp.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
