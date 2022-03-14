from cgitb import text
from email import message
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from telegram import ReplyKeyboardMarkup
from loader import dp
from loader import bot
from keyboards import menu_inline

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    
    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=types.ReplyKeyboardRemove)



