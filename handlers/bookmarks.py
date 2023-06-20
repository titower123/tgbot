import logging

from aiogram import types

from keyboards.bookmarks_keyboard import get_bookmarks_keyboard, bookmark_cb, get_bookmark_keyboard
from loader import dp
from utils.network_tools import send_request, HttpMethod
from .manual_search import message_text


async def get_bookmarks(callback: types.CallbackQuery):
    result = await send_request(f"/users/bookmarks/{callback.from_user.id}", HttpMethod.get, True)
    if result[0] != 200:
        logging.error(f"{result[0]}|{result[1]}")
        await callback.message.answer("Произошла ошибка")
        return
    bookmarks = result[1]
    await callback.message.edit_text("Избранные направления", reply_markup=get_bookmarks_keyboard(bookmarks))


async def get_bookmark(callback: types.CallbackQuery, direction_id):
    result_get_bookmarks = await send_request(f"/users/bookmarks/{callback.from_user.id}", HttpMethod.get, True)
    if result_get_bookmarks[0] != 200:
        logging.error(f"{result_get_bookmarks[0]}|{result_get_bookmarks[1]}")
        await callback.message.answer("Произошла ошибка!")
        return
    result_get_direction = await send_request(f"/directions/{direction_id}", HttpMethod.get, auth=False)
    if result_get_direction[0] != 200:
        logging.error(f"{result_get_bookmarks[0]}|{result_get_bookmarks[1]}")
        await callback.message.answer("Произошла ошибка!")
        return
    bookmarks = result_get_bookmarks[1]
    direction = result_get_direction[1]

    await callback.message.edit_text(message_text(direction=direction),
                                     reply_markup=get_bookmark_keyboard(bookmarks, direction, direction_id))


@dp.callback_query_handler(bookmark_cb.filter())
async def bookmark_inline_keyboard_controller(callback: types.CallbackQuery, callback_data: dict):
    direction_id = callback_data["direction_id"]
    action = callback_data["action"]
    # Удалить направление
    if action == 'delete_bookmark':
        result = await send_request("/users/bookmarks", HttpMethod.delete, True,
                                    {"user_id": callback.from_user.id, "direction_id": direction_id})
        if result[0] != 200:
            logging.error(f"{result[0]}|{result[1]}")
            await callback.answer("Произошла ошибка!", show_alert=True)
            return
        logging.info(
            f'{callback.from_user.id}|{callback.from_user.full_name} - удалил направление {direction_id} из закладок')
        await get_bookmarks(callback)
    if action == 'bookmarks':
        await get_bookmarks(callback)
    if action == 'bookmark':
        await get_bookmark(callback, direction_id)
