from typing import Union
from aiogram import types
from aiogram.types import CallbackQuery
from handlers.doucument_hendler import get_documents
from handlers.filter_hendler import filter_ege
from keyboards.start_keyboard import start_markup
from loader import dp
from keyboards.menu_inline import faculties_keyboard, forma_keyboard, specialization_keyboard, directions_keyboard, \
    direction_keyboard, menu_cd
from utils.db_api.db_commands_hendler import get_direction
from handlers.support_hendler import ask_support
from keyboards.menu_inline import start_menu_cd
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from utils.db_api.db_commands_new_user import add_user,find_user
from utils.notify_admins import notyfi_new_user_add

from utils.strings import HELLO_USER


@dp.message_handler(CommandStart())
async def bot_start(message: Union[types.Message, types.CallbackQuery]):
    if await find_user(message.from_user.id):
        await notyfi_new_user_add(dp=dp, user_id=message.from_user.id, full_name=message.from_user.full_name)
        await add_user(user_id=message.from_user.id, full_name=message.from_user.full_name)
    if isinstance(message, types.Message):
        await message.answer(text=HELLO_USER.format(message.from_user.full_name),
                             reply_markup=start_markup())
    elif isinstance(message, types.CallbackQuery):
        if message.message.text == None:
            await message.message.delete_reply_markup()
            await message.message.answer(text=HELLO_USER.format(message.from_user.full_name),
                                         reply_markup=start_markup())
        else:
            await message.message.edit_text(text=HELLO_USER.format(message.from_user.full_name),
                                            reply_markup=start_markup())


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
    markup = await directions_keyboard(faculties, form, specialization)
    text = "Выберите направление"
    await callback.message.edit_text(text=text, reply_markup=markup)


async def list_direction(callback: types.CallbackQuery, faculties, form, specialization, direction_id):
    markup = await direction_keyboard(faculties, form, specialization, direction_id)
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
        faculties=faculties,
        form=form,
        specialization=specialization,
        direction_id=direction_id
    )


@dp.callback_query_handler(start_menu_cd.filter(), state="*")
async def nav(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()
    button_id = callback_data["button_id"]
    if button_id == "button_EGE":
        await filter_ege(call)
    elif button_id == "button_menu":
        await list_faculties(call)
    elif button_id == "button_question":
        await ask_support(call)
    elif button_id == "button_start":
        await bot_start(call)
    elif button_id == "button_documents":
        await get_documents(call)
