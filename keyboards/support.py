from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from keyboards.menu_inline import start_menu_cd

from data.config import support_ids
from loader import dp

ask_callback = CallbackData("ask_support", "accept_or_cancel")
support_callback = CallbackData("support", "")

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

def get_qusetions_markup():
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text='Получить', callback_data=ask_callback.new(accept_or_cancel='get')),
        InlineKeyboardButton(text='Назад', callback_data=start_menu_cd.new(button_id='button_start'))
    )
    return markup

