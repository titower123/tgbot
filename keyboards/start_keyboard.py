from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from core.config import admins, operators, moderators

start_menu_cd = CallbackData("start_menu", "button_id")


# проверка на пользователя
def who_me(user_id):
    if int(user_id) in admins:
        return admin_start_markup()
    if int(user_id) in moderators:
        return moderator_start_markup()
    if int(user_id) in operators:
        return operator_start_markup()
    return start_markup()

def home_markup():
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=start_menu_cd.new(button_id="button_start"))
    )
    return markup


def start_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="Фильтр по ЕГЭ", callback_data=start_menu_cd.new(button_id="button_EGE")),
        InlineKeyboardButton(text="Ручной поиск направлений", callback_data=start_menu_cd.new(button_id="button_menu")),
        InlineKeyboardButton(text="Избранные направления", callback_data=start_menu_cd.new(button_id="button_bookmarks")),
        InlineKeyboardButton(text="Как подать заявление", callback_data=start_menu_cd.new(button_id="button_documents")),
        InlineKeyboardButton(text="Задать вопрос", callback_data=start_menu_cd.new(button_id="button_question"))
    )
    return markup


def operator_start_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="Фильтр по ЕГЭ",
                             callback_data=start_menu_cd.new(button_id="button_EGE")),
        InlineKeyboardButton(text="Ручной поиск направлений",
                             callback_data=start_menu_cd.new(button_id="button_menu")),
        InlineKeyboardButton(text="Избранные направления",
                             callback_data=start_menu_cd.new(button_id="button_bookmarks")),
        InlineKeyboardButton(text="Как подать заявление",
                             callback_data=start_menu_cd.new(button_id="button_documents")),
        InlineKeyboardButton(text="Получить список новых вопросов",
                             callback_data=start_menu_cd.new(button_id="button_answer")),
        InlineKeyboardButton(text="Побщаться с AI",
                             callback_data=start_menu_cd.new(button_id="button_ai"))
    )
    return markup


def moderator_start_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="Фильтр по ЕГЭ",
                             callback_data=start_menu_cd.new(button_id="button_EGE")),
        InlineKeyboardButton(text="Ручной поиск направлений",
                             callback_data=start_menu_cd.new(button_id="button_menu")),
        InlineKeyboardButton(text="Избранные направления",
                             callback_data=start_menu_cd.new(button_id="button_bookmarks")),
        InlineKeyboardButton(text="Как подать заявление",
                             callback_data=start_menu_cd.new(button_id="button_documents")),
        InlineKeyboardButton(text="Получить неотвеченные вопросы",
                             callback_data=start_menu_cd.new(button_id="button_answer")),
        InlineKeyboardButton(text="Получить отвеченные  вопросы",
                             callback_data=start_menu_cd.new(button_id="button_all_questions")),
        InlineKeyboardButton(text="Побщаться с AI",
                             callback_data=start_menu_cd.new(button_id="button_ai"))
    )
    return markup


def admin_start_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton(text="Фильтр по ЕГЭ",
                             callback_data=start_menu_cd.new(button_id="button_EGE")),
        InlineKeyboardButton(text="Ручной поиск направлений",
                             callback_data=start_menu_cd.new(button_id="button_menu")),
        InlineKeyboardButton(text="Избранные направления",
                             callback_data=start_menu_cd.new(button_id="button_bookmarks")),
        InlineKeyboardButton(text="Как подать заявление",
                             callback_data=start_menu_cd.new(button_id="button_documents")),
        InlineKeyboardButton(text="Получить неотвеченные вопросы",
                             callback_data=start_menu_cd.new(button_id="button_question_admin")),
        InlineKeyboardButton(text="Получить отвеченные  вопросы",
                             callback_data=start_menu_cd.new(button_id="button_all_questions")),
        InlineKeyboardButton(text="Побщаться с AI",
                             callback_data=start_menu_cd.new(button_id="button_ai"))

    )
    return markup
