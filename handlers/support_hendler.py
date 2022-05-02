import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.menu_inline import start_menu_cd
from aiogram.types import ReplyKeyboardRemove
from keyboards.support import ask_callback, support_callback, ask_markup, back_to_menu_markup, get_qusetions_markup
from loader import dp, bot
from states.ask_state import Ask_class
from utils.db_api.db_commands.db_commands_questions import add_question
from data.config import support_ids


async def ask_user(call: types.CallbackQuery):
    await call.message.edit_text(text='Вы можете задать свой вопрос. Оператор ответит вам позже.',
                                 reply_markup=ask_markup())


async def get_questions(call: types.CallbackQuery):
    # проверка на оператора
    if support_ids.count(call.from_user.id) == 1:
        await call.message.edit_text(text='Получить список вопросов', reply_markup=get_qusetions_markup())


#############################################################################################################
###############################################States########################################################
#############################################################################################################

@dp.callback_query_handler(ask_callback.filter())
async def ask_controller(call: types.CallbackQuery, callback_data: dict):
    button_id = callback_data['accept_or_cancel']
    match button_id:
        case 'accept':
            await call.message.edit_text(text='Напишите ваш вопрос')
            await Ask_class.question.set()
        case 'get':
            # TODO: реализовать механизм отправки вопросов
            await call.message.edit_text(text='Отправляю список вопросов')


@dp.message_handler(state=Ask_class.question)
async def ask_message(message: types.Message, state: FSMContext):
    date_time = datetime.datetime.now()
    now = date_time.strftime("[%m/%d/%Y][%H:%M:%S]")
    question = message.text
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    time = now
    await state.finish()
    await add_question(user_id, user_full_name, question, time)
    await message.answer(text='Ваш вопрос был отправлен', reply_markup=back_to_menu_markup())
