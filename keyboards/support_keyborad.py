from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from keyboards.menu_keyboard import start_menu_cd

ask_callback = CallbackData("ask_support", "accept_or_cancel")
support_callback = CallbackData("support", "action", "question_id")


def ask_markup():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text='Написать вопрос', callback_data=ask_callback.new(accept_or_cancel='accept')),
        InlineKeyboardButton(text='Назад', callback_data=start_menu_cd.new(button_id='button_start'))
    )
    return markup


def back_to_menu_markup():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='Назад', callback_data=start_menu_cd.new(button_id='button_start'))
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


def notify_operators_markup():
    return InlineKeyboardMarkup().add(InlineKeyboardButton(text='Посмотреть все вопросы',
                                                           callback_data=ask_callback.new(accept_or_cancel='get')))
