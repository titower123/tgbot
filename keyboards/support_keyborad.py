from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.callback_data import CallbackData

from core.config import admins, operators
from keyboards.start_keyboard import start_menu_cd
from handlers.ai import ai_cb

ask_callback = CallbackData("ask_support", "accept_or_cancel", "data")
support_callback = CallbackData("support", "action", "question_id")


def back_to_menu_markup():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='Вернуться в главное меню', callback_data=start_menu_cd.new(button_id='button_start'))
    )
    return markup


def question_keyboard(question_id: str):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text='Отправить этот вопрос оператору',
                             callback_data=ask_callback.new(accept_or_cancel='forward', data=question_id)),
        InlineKeyboardButton(text='Вернуться в главное меню',
                             callback_data=start_menu_cd.new(button_id='back_to_start'))
    )
    return markup


def get_questions_markup():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='Получить', callback_data=ask_callback.new(accept_or_cancel='get')),
        InlineKeyboardButton(text='Назад', callback_data=start_menu_cd.new(button_id='button_start'))
    )
    return markup


def reply_questions_markup(question_id):
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='Ответить', callback_data=support_callback.new(action='reply',
                                                                                 question_id=question_id)),
        InlineKeyboardButton(text='Отклонить', callback_data=support_callback.new(action='reject',
                                                                                  question_id=question_id))
    )
    return markup


def notify_operators_markup(id):
    if id in admins:
        return InlineKeyboardMarkup().add(InlineKeyboardButton(text='Посмотреть новые вопросы',
                                                               callback_data=start_menu_cd.new(
                                                                   button_id="button_question_admin")))
    elif id in operators:
        return InlineKeyboardMarkup().add(InlineKeyboardButton(text='Посмотреть новые вопросы',
                                                               callback_data=start_menu_cd.new(
                                                                   button_id="button_answer")))
