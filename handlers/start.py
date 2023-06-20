import logging
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from core.strings import HELLO_USER
from utils.misc.notify_admins import notify_new_user_add

from keyboards.start_keyboard import who_me, start_menu_cd
from loader import dp
from .manual_search import get_facutlies
from .bookmarks import get_bookmarks
from utils.network_tools import send_request, HttpMethod


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: Union[types.Message, types.CallbackQuery], state: FSMContext, from_questions: bool=False):
    await state.finish()
    logging.info(f"{message.from_user.id}|{message.from_user.full_name} - в главном меню")
    # добавление новых пользователей в бд
    result = await send_request("/users", HttpMethod.post, json={"user_id": message.from_user.id, "full_name": message.from_user.full_name, "where_from": 0}, auth=True)
    if result[0] == 200:
        await notify_new_user_add(dp, user_id=message.from_user.id, full_name=message.from_user.full_name)
    # разделение на callback и message
    if isinstance(message, types.Message):
        await message.answer(text=HELLO_USER.format(message.from_user.full_name),
                             reply_markup=who_me(message.from_user.id))
    # callback
    elif isinstance(message, types.CallbackQuery):
        # если пользователь возвращается из документов, то...
        if message.message.text is None:
            await message.message.delete_reply_markup()
            await message.message.answer(text=HELLO_USER.format(message.from_user.full_name),
                                         reply_markup=who_me(message.from_user.id))
        # если пользователь вернулся из какого либо другого меню
        else:
            try:
                if not from_questions:
                    await message.message.edit_text(text=HELLO_USER.format(message.from_user.full_name),
                                                    reply_markup=who_me(message.from_user.id))
                else:
                    await message.message.answer(text=HELLO_USER.format(message.from_user.full_name),
                                                    reply_markup=who_me(message.from_user.id))
            except Exception as ex:
                logging.error(ex)


@dp.callback_query_handler(start_menu_cd.filter(), state="*")
async def nav(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    from handlers.doucument_hendler import get_documents
    from handlers.filter_hendler import filter_ege
    from handlers.support_hendler import ask_user, get_questions
    from handlers.support_hendler import get_questions_admin, get_answers_admin
    from handlers.ai import wait_message_form_user
    await state.finish()
    button_id = callback_data["button_id"]

    match button_id:
        case 'button_EGE':
            logging.info(f'{call.from_user.id}|{call.from_user.full_name} - пользователь зашел в фильтр')
            await filter_ege(call)
        case 'button_menu':
            logging.info(f'{call.from_user.id}|{call.from_user.full_name} - пользователь зашел в ручной поиск')
            await get_facutlies(call)
        case 'button_question':
            logging.info(f'{call.from_user.id}|{call.from_user.full_name} - пользователь собирается задать вопрос')
            await ask_user(call)
        case 'button_start':
            await bot_start(call, state)
        case 'button_documents':
            logging.info(f'{call.from_user.id}|{call.from_user.full_name} - пользователь получет pdf')
            await get_documents(call)
        case 'button_answer':
            logging.info(f'{call.from_user.id}|{call.from_user.full_name} - оператор получает вопросы')
            await get_questions(call)
        case 'button_question_admin':
            logging.info(f'{call.from_user.id}|{call.from_user.full_name} - модератор/администратор получет список вопросов')
            await get_questions_admin(call)
        case 'button_bookmarks':
            logging.info(f'{call.from_user.id}|{call.from_user.full_name} - пользователь зашел в закладки')
            await get_bookmarks(call)
        case 'button_all_questions':
            logging.info(f'{call.from_user.id}|{call.from_user.full_name} - модератор/администратор получает список вопросов и ответов')
            await get_answers_admin(call)
        case 'button_ai':
            logging.info(
                f'{call.from_user.id}|{call.from_user.full_name} - пользователь в ai')
            await wait_message_form_user(call)
        case 'back_to_start':
            logging.info(
                f'{call.from_user.id}|{call.from_user.full_name} - пользователь в главном меню')
            await call.message.delete_reply_markup()
            await bot_start(call, state, from_questions=True)

