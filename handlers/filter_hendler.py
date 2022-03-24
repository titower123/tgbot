from loader import dp
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.filter_inline import main_keyboard

async def filter_EGE(call: types.CallbackQuery):
    markup = await main_keyboard()
    await call.message.edit_text("Пункт не готов :(", reply_markup=markup)