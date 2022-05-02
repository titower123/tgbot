from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

start_menu_cd = CallbackData("start_menu", "button_id")


def start_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(
        InlineKeyboardButton(text="Фильтр по ЕГЭ", callback_data=start_menu_cd.new(button_id="button_EGE")),
    )
    markup.row(
        InlineKeyboardButton(text="Ручной поиск направлений", callback_data=start_menu_cd.new(button_id="button_menu")),
    )
    markup.row(
        InlineKeyboardButton(text="Задать вопрос", callback_data=start_menu_cd.new(button_id="button_question")),
        InlineKeyboardButton(text="Как подать заявление", callback_data=start_menu_cd.new(button_id="button_documents"))
    )
    return markup


def operator_start_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(
        InlineKeyboardButton(text="Фильтр по ЕГЭ", callback_data=start_menu_cd.new(button_id="button_EGE")),
    )
    markup.row(
        InlineKeyboardButton(text="Ручной поиск направлений", callback_data=start_menu_cd.new(button_id="button_menu")),
    )
    markup.row(
        InlineKeyboardButton(text="Получить список вопросов",
                             callback_data=start_menu_cd.new(button_id="button_answer")),
        InlineKeyboardButton(text="Как подать заявление", callback_data=start_menu_cd.new(button_id="button_documents"))
    )
    return markup
