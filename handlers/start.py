from typing import Union
from aiogram import types
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Command
from handlers.doucument_hendler import get_documents
from handlers.filter_hendler import filter_EGE
from loader import dp
from keyboards.menu_inline import faculties_keyboard, forma_keyboard,specialization_keyboard ,directions_keyboard,direction_keyboard, menu_cd
from utils.db_api.db_commands import get_direction
from handlers.support_hendler import ask_support
from keyboards.menu_inline import start_menu_cd
from aiogram.dispatcher.filters.builtin import CommandStart


def start_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(
        InlineKeyboardButton(text="Фильтр по ЕГЭ", callback_data=start_menu_cd.new(button_id="button_EGE")),
        InlineKeyboardButton(text="Ручной поиск", callback_data=start_menu_cd.new(button_id="button_menu")),
    )
    markup.row(
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



async def list_faculties(message: CallbackQuery, **kwargs):
    markup = await faculties_keyboard()
    await message.message.edit_text(text="Выбирте факультет", reply_markup=markup)

async def list_forma(callback: types.CallbackQuery, faculties, **kwargs):
    markup = await forma_keyboard(faculties)
    text = "Выберите форму обучения"
    await callback.message.edit_text(text=text, reply_markup=markup)

async def list_specialization(callback: types.CallbackQuery, faculties, form, **kwargs):
    markup = await specialization_keyboard(faculties, form)
    text = "Выберите специальность"
    await callback.message.edit_text(text=text, reply_markup=markup)

async def list_directions(callback: types.CallbackQuery, faculties, form, specialization, **kwargs):
    markup = await directions_keyboard(faculties,form, specialization)
    text="Выберите направление"
    await callback.message.edit_text(text=text, reply_markup=markup)

async def list_direction(callback: types.CallbackQuery, faculties, form, specialization, direction_id):
    markup = await direction_keyboard(faculties,form,specialization,direction_id)
    direction = await get_direction(direction_id)
    text = f"""<b>{direction.name}</b>\n\n{str(direction.description)}"""
    await callback.message.edit_text(text=text, reply_markup=markup)

@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: types.CallbackQuery, callback_data: dict):
    current_level = callback_data.get('level')
    faculties = callback_data.get('faculties')
    form = callback_data.get('form')
    specialization = callback_data.get('specialization')
    direction_id = int(callback_data.get('direction_id'))

    levels = {
        "0": list_faculties,
        "1": list_forma,
        "2": list_specialization,
        "3": list_directions,
        "4": list_direction
    }

    func_cur_level = levels[current_level]
    await func_cur_level(
        call,
        faculties = faculties,
        form = form,
        specialization = specialization,
        direction_id = direction_id
    )

@dp.callback_query_handler(start_menu_cd.filter())
async def nav(call: types.CallbackQuery, callback_data: dict):
    button_id = callback_data["button_id"]
    if button_id == "button_EGE":
        await filter_EGE(call)
    elif button_id == "button_menu":
        await list_faculties(call)
    elif button_id == "button_question":
        await ask_support(call)
    elif button_id == "button_start":
        await bot_start(call)
    elif button_id == "button_documents":
        await get_documents(call)
        

