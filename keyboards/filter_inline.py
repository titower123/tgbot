from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from keyboards.menu_inline import start_menu_cd

filter_cd = CallbackData('filter', 'subject_id')

async def main_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(text="Русский язык", callback_data=filter_cd.new(subject_id='russian')),
        InlineKeyboardButton(text="Физика", callback_data=filter_cd.new(subject_id='physics')),
        InlineKeyboardButton(text="Биология", callback_data=filter_cd.new(subject_id='biology')),
        InlineKeyboardButton(text="Химия", callback_data=filter_cd.new(subject_id='chemistry')),
        InlineKeyboardButton(text="Математика", callback_data=filter_cd.new(subject_id='maths')),
        InlineKeyboardButton(text="Обществознание", callback_data=filter_cd.new(subject_id='social')),
    )
    markup.add(
        InlineKeyboardButton(text="История", callback_data=filter_cd.new(subject_id='history')),
        InlineKeyboardButton(text="Иностранный язык", callback_data=filter_cd.new(subject_id='language')),
        InlineKeyboardButton(text="Информатика и ИКТ", callback_data=filter_cd.new(subject_id='informat')),
        InlineKeyboardButton(text="Литература", callback_data=filter_cd.new(subject_id='literature')),
        InlineKeyboardButton(text="Творческое испытание", callback_data=filter_cd.new(subject_id='trial')),
    )
    markup.row(
        InlineKeyboardButton(text="Найти", callback_data=start_menu_cd.new(button_id='button_start')),
    )
    markup.row(
        InlineKeyboardButton(text='Назад', callback_data=start_menu_cd.new(button_id='button_start'))
    )
    return markup
