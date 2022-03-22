from typing import Union
from aiogram import types
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.filters import Command
from loader import dp
from keyboards.menu_inline import faculties_keyboard, forma_keyboard,specialization_keyboard ,directions_keyboard,direction_keyboard, menu_cd
from utils.db_api.db_commands import get_direction
from handlers.start import bot_start
from keyboards.menu_inline import start_menu_cd

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
async def navi(call: types.CallbackQuery, callback_data: dict):
    button_id = callback_data["button_id"]
    if button_id == "button_start":
        bot_start(call)

