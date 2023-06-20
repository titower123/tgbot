import datetime
import logging
from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext

from core.strings import ASK_CONTROLLER_ACCEPT, ASK_CONTROLLER_GET, ASK_CONTROLLER_QUESTION, \
    ASK_MESSAGE, REJECT_QUESTION_OPERATOR, REJECT_QUESTION_USER, REPLY_QUESTION_OPERATOR, REPLY_SENT, REPLY_RESEIVED, \
    ASK_CONTROLLER_QUESTION_ADMIN, NO_NEW_QUESTIONS, QUESTION_ANSWER
from keyboards.start_keyboard import home_markup
from keyboards.support_keyborad import ask_callback, support_callback, back_to_menu_markup, \
    reply_questions_markup, question_keyboard
from loader import dp, bot
from states.ask_state import AskClass
from states.support_state import SupportClass
from utils.misc.notify_operators import notify_new_question
from utils.network_tools import send_request, HttpMethod

question_delay = {}


# Абитуриент задает вопрос
async def ask_user(call: types.CallbackQuery):
    await call.message.edit_text(text=ASK_CONTROLLER_ACCEPT)
    await AskClass.question.set()


# Оператор получает список вопросов
async def get_questions(call: types.CallbackQuery):
    result = await send_request("/faq/questions", HttpMethod.get, True)
    if result[0] != 200:
        logging.error(f"{result[0]}|{result[1]}")
        await call.answer("Произошла ошибка!", show_alert=True)
        return
    questions = result[1]
    count = 0
    for question in questions:
        await call.message.answer(ASK_CONTROLLER_QUESTION.format(
            datetime.strptime(question["time_of_receipt_of_the_question"], '%Y-%m-%dT%H:%M:%S.%f')
            .strftime("%d/%m/%Y - %H:%M"),
            question["user"]["full_name"],
            question["question"]),
            reply_markup=reply_questions_markup(question_id=question["id"]))
        count += 1
    if count == 0:
        await call.message.edit_text(text=NO_NEW_QUESTIONS, reply_markup=home_markup())
    else:
        await call.message.edit_text(text=ASK_CONTROLLER_GET)


# Админ смотрит вопросы без ответов
async def get_questions_admin(call: types.CallbackQuery):
    result = await send_request("/faq/questions", HttpMethod.get, True)
    if result[0] != 200:
        logging.error(f"{result[0]}|{result[1]}")
        await call.answer("Произошла ошибка!", show_alert=True)
        return
    questions = result[1]
    count = 0
    for quest in questions:
        if quest["answer"] is None:
            await call.message.answer(ASK_CONTROLLER_QUESTION_ADMIN.format(
                quest["id"],
                quest["user"]["full_name"],
                quest["user"]["user_id"],
                datetime.strptime(quest["time_of_receipt_of_the_question"], '%Y-%m-%dT%H:%M:%S.%f').strftime(
                    "%d/%m/%Y - %H:%M"),
                quest["question"]
            ))
            count += 1
    if count == 0:
        await call.message.edit_text(text=NO_NEW_QUESTIONS, reply_markup=home_markup())
    else:
        await call.message.edit_text(text=ASK_CONTROLLER_GET)


# Админ или модератор получают список вопросов с ответами
async def get_answers_admin(call: types.CallbackQuery):
    result = await send_request("/faq/questions_and_true_answers", HttpMethod.get, True)
    if result[0] != 200:
        logging.error(f"{result[0]}|{result[1]}")
        await call.answer("Произошла ошибка!", show_alert=True)
        return
    await call.message.edit_text("Показываю последние 2 вопроса")
    questions = result[1]
    if len(questions) > 0:
        for quest in questions[-2:]:
            await call.message.answer(QUESTION_ANSWER.format(
                quest["answer"]["operator"]["full_name"],
                quest["user"]["full_name"],
                datetime.strptime(quest["time_of_receipt_of_the_question"], '%Y-%m-%dT%H:%M:%S.%f').strftime(
                    "%d/%m/%Y - %H:%M"),
                datetime.strptime(quest["answer"]["response_time"], '%Y-%m-%dT%H:%M:%S.%f').strftime(
                    "%d/%m/%Y - %H:%M"),
                quest["question"],
                quest["answer"]["answer"]
            ))
    else:
        await call.message.edit_text(text=NO_NEW_QUESTIONS, reply_markup=home_markup())


#############################################################################################################
###############################################States########################################################
#############################################################################################################


# Контроллер
@dp.callback_query_handler(ask_callback.filter(), state=AskClass.question)
async def ask_controller(call: types.CallbackQuery, callback_data: dict):
    button_id = callback_data['accept_or_cancel']
    match button_id:
        case 'forward':
            logging.info(
                f'{call.from_user.id}|{call.from_user.full_name} - пользователь перенаправил вопрос оператору')
            if question_delay.get(call.from_user.id) is None:
                question_delay[call.from_user.id] = datetime.now()
            data = callback_data['data']
            result = await send_request(f'/faq/forward_question/{data}', HttpMethod.post, True)
            if result[0] != 200:
                logging.error(f"{result[0]}|{result[1]}")
                await call.answer("Произошла ошибка!")
                return
            await notify_new_question(dp)  # оповещаем оператора о наличии нового вопроса
            await call.message.edit_text(text=ASK_MESSAGE, reply_markup=back_to_menu_markup())


@dp.message_handler(state=AskClass.question)
async def ask_message(message: types.Message, state: FSMContext):
    logging.info(f'{message.from_user.id}|{message.from_user.full_name} - пользователь задал вопрос - {message.text}')
    user_time: datetime = question_delay.get(message.from_user.id)
    if user_time is not None:
        if (datetime.now() - user_time) > timedelta(hours=12):
            question_delay.pop(message.from_user.id)
    user_time: datetime = question_delay.get(message.from_user.id)
    if user_time is not None:
        logging.info(
            f'{message.from_user.id}|{message.from_user.full_name} - вопрос ушел оператору')
        result = await send_request('/faq/new_question', HttpMethod.post, True,
                                    {
                                        "question": message.text,
                                        "message_id": int(message.message_id),
                                        "user_id": int(message.from_user.id)
                                    }
                                    )
        if result[0] != 200:
            await state.finish()
            logging.error(f"{result[0]}|{result[1]}")
            await message.answer("Произошла ошибка!")
            return
        await state.finish()
        await notify_new_question(dp)  # Оповещаем оператора о наличии нового вопроса
        await message.answer(text=ASK_MESSAGE, reply_markup=back_to_menu_markup())
    else:
        logging.info(
            f'{message.from_user.id}|{message.from_user.full_name} - вопрос ушел ии')
        await message.answer_chat_action("typing")
        # Отправка вопроса на сервер
        result = await send_request('/faq/new_question_to_ai', HttpMethod.post, True,
                                    {
                                        "question": message.text,
                                        "message_id": int(message.message_id),
                                        "user_id": int(message.from_user.id)
                                    }
                                    )
        # Проверка на то что ии не сработал
        if result[0] == 302:
            logging.info(
                f'{message.from_user.id}|{message.from_user.full_name} - ии не смог ответить. вопрос ушел оператору')
            await state.finish()
            await notify_new_question(dp)  # Оповещаем оператора о наличии нового вопроса
            await message.answer(text=ASK_MESSAGE, reply_markup=back_to_menu_markup())
            return
        # Проверка при возникновении ошибки
        if result[0] != 200:
            await state.finish()
            logging.error(f"{result[0]}|{result[1]}")
            await message.answer("Произошла ошибка!")
            return
        logging.info(
            f'{message.from_user.id}|{message.from_user.full_name} - ии ответил на вопрос. [{result[1]["message"]}]')
        await message.answer(text=result[1]["message"] + "<u>\nЭто сообщение сгенерировал искусственный интеллект! Вы "
                                                         "можете перенаправить сообщение оператору, если ответ "
                                                         "выдаваемый ИИ не точный</u>",
                             reply_markup=question_keyboard(result[1]["id"]))


# Контроллер вопроса (ответить/отклонить)
@dp.callback_query_handler(support_callback.filter())
async def support_controller(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    action = callback_data['action']
    question_id = callback_data['question_id']
    result = await send_request(f"/faq/question/{question_id}", HttpMethod.get, True)
    if result[0] != 200:
        logging.error(f"{result[0]}|{result[1]}")
        await call.message.answer("Произошла ошибка!")
        return
    question = result[1]
    match action:
        case 'reject':
            logging.info(
                f'{call.from_user.id}|{call.from_user.full_name} - оператор отклонил вопрос')
            await call.message.edit_text(REJECT_QUESTION_OPERATOR)
            # оповещаем пользователя о том что его вопрос был отклонен
            await bot.send_message(chat_id=question['user']['user_id'], text=REJECT_QUESTION_USER,
                                   reply_to_message_id=question['message_id'])
            result = await send_request(f"/faq/new_answer", HttpMethod.post, True,
                                        {"answer": 'ОТКЛОНЕН', "operator_id": int(call.from_user.id),
                                         "question_id": question_id})
            if result[0] != 200:
                logging.error(f"{result[0]}|{result[1]}")
                await call.answer("Произошла ошибка!", show_alert=True)
                return
            # await delete_question(question_id)
        case 'reply':
            logging.info(
                f'{call.from_user.id}|{call.from_user.full_name} - оператор пишет ответ на вопрос')
            await call.message.delete_reply_markup()
            await call.message.answer(REPLY_QUESTION_OPERATOR)
            await SupportClass.answer.set()
            await state.set_data({'question_id': question_id})


@dp.message_handler(state=SupportClass.answer)
async def support_state(message: types.Message, state: FSMContext):
    answer = message.text
    # получаем из state номер вопроса
    question_id_from_state = await state.get_data()
    await state.finish()
    question_id = question_id_from_state['question_id']
    result = await send_request(f"/faq/question/{question_id}", HttpMethod.get, True)
    if result[0] != 200:
        logging.error(f"{result[0]}|{result[1]}")
        await message.answer("Произошла ошибка!")
        return
    question = result[1]
    await message.answer(REPLY_SENT)
    # отправляем ответ на вопрос пользователю
    await bot.send_message(chat_id=int(question['user']['user_id']), text=REPLY_RESEIVED.format(answer),
                           reply_to_message_id=int(question['message_id']))
    # Добавляем вопрос в таблицу всех вопросов
    result = await send_request(f"/faq/new_answer", HttpMethod.post, True,
                                {"answer": answer, "operator_id": int(message.from_user.id),
                                 "question_id": question_id})
    logging.info(
        f'{message.from_user.id}|{message.from_user.full_name} - оператор ответил на вопрос [{answer}]')
    if result[0] != 200:
        logging.error(f"{result[0]}|{result[1]}")
        await message.answer("Произошла ошибка!")
        return
