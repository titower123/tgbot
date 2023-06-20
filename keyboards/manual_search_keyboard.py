from aiogram import types
from aiogram.utils.callback_data import CallbackData

from keyboards.start_keyboard import start_menu_cd

directions_cb = CallbackData("directions_menu", "level", "object_id", "back")


def make_directions_cd(level, object_id="0", back="0"):
    return directions_cb.new(level=level, object_id=object_id, back=back)


def get_faculties_keyboard(faculties):
    CURRENT_LEVEL = 0
    markup = types.InlineKeyboardMarkup(row_width=1)
    for item in faculties:
        button_text = item["name"]
        markup.insert(
            types.InlineKeyboardButton(text=button_text,
                                       callback_data=make_directions_cd(CURRENT_LEVEL + 1, item["id"]))
        )
    markup.row(
        types.InlineKeyboardButton(text="Назад", callback_data=start_menu_cd.new(button_id='button_start'))
    )
    return markup


def get_forms_of_study_keyboard(forms_of_study):
    CURRENT_LEVEL = 1
    markup = types.InlineKeyboardMarkup(row_width=1)
    for item in forms_of_study:
        markup.insert(
            types.InlineKeyboardButton(text=item["name"],
                                       callback_data=make_directions_cd(CURRENT_LEVEL + 1, item["id"]))
        )
    markup.row(types.InlineKeyboardButton(text="Назад", callback_data=make_directions_cd(CURRENT_LEVEL - 1)))
    return markup


def get_qualifications_keyboard(qualifications):
    CURRENT_LEVEL = 2
    markup = types.InlineKeyboardMarkup(row_width=1)
    for item in qualifications:
        markup.insert(
            types.InlineKeyboardButton(text=item["name"],
                                       callback_data=make_directions_cd(CURRENT_LEVEL + 1, item["id"]))
        )
    markup.row(
        types.InlineKeyboardButton(text="Назад", callback_data=make_directions_cd(CURRENT_LEVEL - 1,
                                                                                  qualifications[0]["form_of_study_id"],
                                                                                  "1")))
    return markup


def get_directions_keyboard(directions):
    CURRENT_LEVEL = 3
    markup = types.InlineKeyboardMarkup(row_width=1)
    for item in directions:
        markup.insert(
            types.InlineKeyboardButton(text=item["name"],
                                       callback_data=make_directions_cd(CURRENT_LEVEL + 1, item["id"])))
    markup.row(
        types.InlineKeyboardButton(text="Назад",
                                   callback_data=make_directions_cd(CURRENT_LEVEL - 1,
                                                                    directions[0]["qualification_id"], "1")))
    return markup


def get_direction_keyboard(bookmarks, direction):
    CURRENT_LEVEL = 4
    markup = types.InlineKeyboardMarkup(row_width=1)
    if bookmarks is not []:
        bookmark_ids = [bookmark["id"] for bookmark in bookmarks]
        if direction["id"] in bookmark_ids:
            markup.add(
                types.InlineKeyboardButton(text="Удалить из избранного",
                                           callback_data=make_directions_cd(CURRENT_LEVEL + 2, direction["id"])))
        else:
            markup.add(
                types.InlineKeyboardButton(text="Добавить в избранное",
                                           callback_data=make_directions_cd(CURRENT_LEVEL + 1, direction["id"])))
    else:
        markup.add(types.InlineKeyboardButton(text="Добавить в избранное",
                                              callback_data=make_directions_cd(CURRENT_LEVEL + 1, direction["id"])))
    markup.row(
        types.InlineKeyboardButton(text="Назад",
                                   callback_data=make_directions_cd(CURRENT_LEVEL - 1, direction["qualification_id"],
                                                                    "1")),
    )
    return markup
