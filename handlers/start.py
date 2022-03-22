from typing import Union
from aiogram import types
import aiogram
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters.builtin import CommandStart
from handlers.menu_handlers import list_faculties
from loader import dp
from keyboards.menu_inline import start_menu_cd




def start_markup():
    markup = InlineKeyboardMarkup()
    markup.row(
    InlineKeyboardButton(text="Фильтр по ЕГЭ", callback_data=start_menu_cd.new(button_id="button_EGE")),
    InlineKeyboardButton(text="Ручной поиск", callback_data=start_menu_cd.new(button_id="button_menu")),
    InlineKeyboardButton(text="Задать вопрос", callback_data=start_menu_cd.new(button_id="button_question")),
    InlineKeyboardButton(text="Документы для поступления", callback_data=start_menu_cd.new(button_id="button_documents"))
    )
    return markup

@dp.message_handler(CommandStart())
async def bot_start(message: Union[(types.Message),(types.CallbackQuery)]):
    if isinstance(message, types.Message):
        await message.answer(f"Привет, {message.from_user.full_name}! Я помогу тебе с выбором.", reply_markup=start_markup())
    elif isinstance(message, types.CallbackQuery):
        await message.message.edit_text(text=f"Привет, {message.from_user.full_name}! Я помогу тебе с выбором.", reply_markup=start_markup())
    


@dp.callback_query_handler(start_menu_cd.filter())
async def nav(call: types.CallbackQuery, callback_data: dict):
    button_id = callback_data["button_id"]
    if button_id == "button_EGE":
        pass
    elif button_id == "button_menu":
        await list_faculties(call)
    elif button_id == "button_question":
        pass
    else:
        pass





