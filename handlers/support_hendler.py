import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.support_keyborad import ask_callback, support_callback, ask_markup, back_to_menu_markup,\
    get_questions_markup, reply_questions_markup
from loader import dp, bot
from states.ask_state import AskClass
from states.support_state import SupportClass
from utils.db_api.db_commands.db_commands_questions import add_question, count_questions, all_questions, \
    delete_question, get_data_question
from data.config import OPERATORS_IDS
from utils.notify_operators import notify_new_question
from data.strings import ASK_USER, GET_QUESTIONS, ASK_CONTROLLER_ACCEPT, ASK_CONTROLLER_GET, ASK_CONTROLLER_QUESTION, \
    ASK_MESSAGE, REJECT_QUESTION_OPERATOR, REJECT_QUESTION_USER, REPLY_QUESTION_OPERATOR, REPLY_SENT, REPLY_RESEIVED


async def ask_user(call: types.CallbackQuery):
    await call.message.edit_text(text=ASK_USER,
                                 reply_markup=ask_markup())


async def get_questions(call: types.CallbackQuery):
    # проверка на оператора
    if OPERATORS_IDS.count(str(call.from_user.id)) == 1:
        await call.message.edit_text(text=GET_QUESTIONS, reply_markup=get_questions_markup())


#############################################################################################################
###############################################States########################################################
#############################################################################################################

@dp.callback_query_handler(ask_callback.filter())
async def ask_controller(call: types.CallbackQuery, callback_data: dict):
    button_id = callback_data['accept_or_cancel']
    match button_id:
        case 'accept':
            await call.message.edit_text(text=ASK_CONTROLLER_ACCEPT)
            await AskClass.question.set()
        case 'get':
            count_quest = await count_questions()
            await call.message.edit_text(text=ASK_CONTROLLER_GET.format(count_quest))
            list_quest = await all_questions()
            for quest in list_quest:
                await call.message.answer(ASK_CONTROLLER_QUESTION.format(quest.question),
                                          reply_markup=reply_questions_markup(question_id=quest.id))


@dp.message_handler(state=AskClass.question)
async def ask_message(message: types.Message, state: FSMContext):
    date_time = datetime.datetime.now()
    now = date_time.strftime("[%m/%d/%Y][%H:%M:%S]")
    question = message.text
    user_id = message.from_user.id
    message_id = message.message_id
    time = now
    await state.finish()
    await add_question(user_id, message_id, question, time)
    await notify_new_question(dp)  # оповвещаем оператора о наличии нового вопроса
    await message.answer(text=ASK_MESSAGE, reply_markup=back_to_menu_markup())


@dp.callback_query_handler(support_callback.filter())
async def support_controller(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    action = callback_data['action']
    question_id = callback_data['question_id']
    data = await get_data_question(int(question_id))
    match action:
        case 'reject':
            await call.message.edit_text(REJECT_QUESTION_OPERATOR)
            # оповещаем пользователя о том что его вопрос был отклонен
            await bot.send_message(chat_id=data.user_id, text=REJECT_QUESTION_USER,
                                   reply_to_message_id=data.message_id)
            await delete_question(question_id)
        case 'reply':
            await call.message.delete_reply_markup()
            await call.message.answer(REPLY_QUESTION_OPERATOR)
            await SupportClass.answer.set()
            await state.set_data({'question_id': question_id})


@dp.message_handler(state=SupportClass.answer)
async def support_state(message: types.Message, state: FSMContext):
    text = message.text
    # получаем из state номер вопроса
    list = await state.get_data()
    await state.finish()
    question_id = list['question_id']
    data = await get_data_question(int(question_id))
    await message.answer(REPLY_SENT)
    # отправляем ответ на вопрос пользователю
    await bot.send_message(chat_id=int(data.user_id), text=REPLY_RESEIVED.format(text),
                           reply_to_message_id=int(data.message_id))
    # удаляем вопрос из БД
    await delete_question(int(question_id))
