from aiogram import types
from aiogram.utils.callback_data import CallbackData

from keyboards.start_keyboard import start_menu_cd

bookmark_cb = CallbackData("bookmark", "direction_id", "action")


def get_bookmarks_keyboard(bookmarks):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for bookmark in bookmarks:
        markup.add(
            types.InlineKeyboardButton(bookmark["name"],
                                       callback_data=bookmark_cb.new(direction_id=bookmark["id"], action="bookmark"))
        )
        markup.add(
            types.InlineKeyboardButton("Назад", callback_data=start_menu_cd.new(button_id='button_start'))
        )
    return markup


def get_bookmark_keyboard(bookmarks, direction, direction_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    if bookmarks is not []:
        bookmark_ids = [bookmark["id"] for bookmark in bookmarks]
        if direction["id"] in bookmark_ids:
            markup.add(
                types.InlineKeyboardButton(text="Удалить из избранного",
                                           callback_data=bookmark_cb.new(direction_id=direction_id,
                                                                         action="delete_bookmark"))
            )
    markup.row(
        types.InlineKeyboardButton(text="Назад",
                                   callback_data=bookmark_cb.new(direction_id=direction_id, action="bookmarks")),

    )
    return markup
