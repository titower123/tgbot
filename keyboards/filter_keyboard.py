import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from keyboards.start_keyboard import start_menu_cd
from utils.network_tools import HttpMethod, send_request

filter_cd = CallbackData('filter', 'subject_id')

direction_cd = CallbackData("direction_menu", "level", 'user_id', "direction_id")

# запрос пользователя с id предметов


def make_direction_cd(level, user_id="0", direction_id="0"):
    return direction_cd.new(level=level, user_id=user_id, direction_id=direction_id)

#TODO: подумать над автогенирацией клавиатуры
def main_keyboard():
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
        InlineKeyboardButton(text="География", callback_data=filter_cd.new(subject_id='География'))
    )
    markup.row(
        InlineKeyboardButton(text="Найти", callback_data=filter_cd.new(subject_id='Найти')),
        InlineKeyboardButton(text='Сброс', callback_data=filter_cd.new(subject_id='Сброс'))
    ),
    markup.row(
        InlineKeyboardButton(text='Назад', callback_data=start_menu_cd.new(button_id='button_start'))
    )
    return markup


async def filter_directions_keyboard(directions, user_id):
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup(row_width=1)
    for direction in directions:
        button_text = direction["name"]
        callback_data = make_direction_cd(level=CURRENT_LEVEL + 1, user_id=user_id, direction_id=direction["id"])
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=start_menu_cd.new(button_id='button_EGE'))
    )
    return markup


async def filter_direction_keyboard(user_id, direction_id):
    CURRENT_LEVEL = 2
    result_get_bookmarks = await send_request(f"/users/bookmarks/{user_id}", HttpMethod.get, True)
    if result_get_bookmarks[0] != 200:
        logging.error(f"{result_get_bookmarks[0]}|{result_get_bookmarks[1]}")
        return
    result_get_direction = await send_request(f"/directions/{direction_id}", HttpMethod.get, auth=False)
    if result_get_direction[0] != 200:
        logging.error(f"{result_get_bookmarks[0]}|{result_get_bookmarks[1]}")
        return
    markup = InlineKeyboardMarkup()
    bookmarks = result_get_bookmarks[1]
    direction = result_get_direction[1]
    if bookmarks is not []:
        bookmark_ids = [bookmark["id"] for bookmark in bookmarks]
        if direction["id"] in bookmark_ids:
            markup.add(
                InlineKeyboardButton(text="Удалить из избранного",
                                           callback_data=make_direction_cd(level=CURRENT_LEVEL + 2,direction_id=direction_id))
            )
        else:
            markup.add(
                InlineKeyboardButton(text="Добавить в избранное",
                                       callback_data=make_direction_cd(level=CURRENT_LEVEL+1, direction_id=direction_id))
            )
    else:
        markup.add(InlineKeyboardButton(text="Добавить в избранное",
                                   callback_data=make_direction_cd(level=CURRENT_LEVEL+1, direction_id=direction_id))
                   )
    markup.row(
        InlineKeyboardButton(text="Назад",
                             callback_data=make_direction_cd(level=CURRENT_LEVEL - 1, user_id=user_id))
    )
    return markup

