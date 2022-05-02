from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from keyboards.start_keyboard import start_menu_cd
from states.filter_state import user_request
from utils.db_api.db_commands.db_commands_hendler import get_direction

filter_cd = CallbackData('filter', 'subject_id')

direction_cd = CallbackData("direction_menu", "level", 'user_id', "direction_id")


def make_direction_cd(level, user_id="0", direction_id="0"):
    return direction_cd.new(level=level, user_id=user_id, direction_id=direction_id)


async def main_keyboard():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton(text="Русский язык", callback_data=filter_cd.new(subject_id='Русский язык')),
        InlineKeyboardButton(text="Физика", callback_data=filter_cd.new(subject_id='Физика')),
        InlineKeyboardButton(text="Биология", callback_data=filter_cd.new(subject_id='Биология')),
        InlineKeyboardButton(text="Химия", callback_data=filter_cd.new(subject_id='Химия')),
        InlineKeyboardButton(text="Математика", callback_data=filter_cd.new(subject_id='Математика')),
        InlineKeyboardButton(text="Обществознание", callback_data=filter_cd.new(subject_id='Обществознание')),
    )
    markup.add(
        InlineKeyboardButton(text="История", callback_data=filter_cd.new(subject_id='История')),
        InlineKeyboardButton(text="Иностранный язык", callback_data=filter_cd.new(subject_id='Иностранный язык')),
        InlineKeyboardButton(text="Информатика и ИКТ", callback_data=filter_cd.new(subject_id='Информатика и ИКТ')),
        InlineKeyboardButton(text="Литература", callback_data=filter_cd.new(subject_id='Литература')),
        InlineKeyboardButton(text="Творческое испытание",
                             callback_data=filter_cd.new(subject_id='Творческое испытание')),
    )
    markup.row(
        InlineKeyboardButton(text="Найти", callback_data=filter_cd.new(subject_id='Найти'))
    ),
    markup.row(
        InlineKeyboardButton(text='Назад', callback_data=start_menu_cd.new(button_id='button_start'))
    )
    return markup


async def filter_directions_keyboard(user_id):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=1)
    directions = user_request.get(int(user_id))
    for direction in directions:
        item = await get_direction(int(direction))
        button_text = item.name
        callback_data = make_direction_cd(level=CURRENT_LEVEL + 1, user_id=user_id, direction_id=item.id)
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )

    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=start_menu_cd.new(button_id='button_EGE'))
    )
    return markup


async def filter_direction_keyboard(user_id, direction_id):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text="Назад",
                             callback_data=make_direction_cd(level=CURRENT_LEVEL - 1, user_id=user_id))
    )
    return markup
