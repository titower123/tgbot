import logging

from aiogram import types

from core.strings import message_text
from keyboards.manual_search_keyboard import get_faculties_keyboard, get_forms_of_study_keyboard, \
    get_qualifications_keyboard, get_directions_keyboard, get_direction_keyboard, directions_cb
from loader import dp
from utils.network_tools import send_request, HttpMethod


async def get_facutlies(callback: types.CallbackQuery):
    result = await send_request("/faculties", method=HttpMethod.get, auth=False)
    if result[0] != 200:
        logging.error(f"{result[0]}|{result[1]}")
        await callback.answer("Произошла ошибка", show_alert=True)
        return
    faculties = result[1]
    await callback.message.edit_text("Факультеты", reply_markup=get_faculties_keyboard(faculties))


async def get_form_of_study(callback: types.CallbackQuery, object_id):
    result = await send_request(f"/faculties/{object_id}?collection=true", HttpMethod.get, auth=False)
    if result[0] != 200:
        logging.error(f"{result[0]}|{result[1]}")
        await callback.answer("Произошла ошибка", show_alert=True)
        return
    forms_of_study = result[1]
    await callback.message.edit_text("Форма обучения", reply_markup=get_forms_of_study_keyboard(forms_of_study))


async def get_qualifications(callback: types.CallbackQuery, object_id):
    result = await send_request(f"/formsOfStudy/{object_id}?collection=true", HttpMethod.get, auth=False)
    if result[0] != 200:
        logging.error(f"{result[0]}|{result[1]}")
        await callback.answer("Произошла ошибка", show_alert=True)
        return
    qualifications = result[1]
    await callback.message.edit_text("Уровни образования", reply_markup=get_qualifications_keyboard(qualifications))


async def get_directions(callback: types.CallbackQuery, object_id):
    result = await send_request(f"/qualifications/{object_id}?collection=true", HttpMethod.get, auth=False)
    if result[0] != 200:
        logging.error(f"{result[0]}|{result[1]}")
        await callback.answer("Произошла ошибка", show_alert=True)
        return
    directions = result[1]
    await callback.message.edit_text("Направления", reply_markup=get_directions_keyboard(directions))


async def get_direction(callback: types.CallbackQuery, object_id):

    result_get_bookmarks = await send_request(f"/users/bookmarks/{callback.from_user.id}", HttpMethod.get, True)
    if result_get_bookmarks[0] != 200:
        logging.error(f"{result_get_bookmarks[0]}|{result_get_bookmarks[1]}")
        await callback.message.answer("Произошла ошибка!")
        return
    result_get_direction = await send_request(f"/directions/{object_id}", HttpMethod.get, auth=False)
    if result_get_direction[0] != 200:
        logging.error(f"{result_get_bookmarks[0]}|{result_get_bookmarks[1]}")
        await callback.message.answer("Произошла ошибка!")
        return
    bookmarks = result_get_bookmarks[1]
    direction = result_get_direction[1]


    await callback.message.edit_text(message_text(direction), reply_markup=get_direction_keyboard(bookmarks, direction))


@dp.callback_query_handler(directions_cb.filter())
async def directions_menu_keyboard_controller(callback: types.CallbackQuery, callback_data: dict):
    current_level = int(callback_data['level'])
    object_id = callback_data['object_id']
    back = callback_data['back']
    match current_level:
        case 0:
            await get_facutlies(callback)
        case 1:
            if back == '1':
                print(object_id)
                result = await send_request(f"/formsOfStudy/{object_id}?collection=false", HttpMethod.get, False)
                if result[0] != 200:
                    logging.error(f"{result[0]}|{result[1]}")
                    await callback.answer("Произошла ошибка!", show_alert=True)
                    return
                faculty = result[1]
                object_id = faculty["faculty_id"]
                print(object_id)
            await get_form_of_study(callback, object_id)
        case 2:
            if back == '1':
                result = await send_request(f"/qualifications/{object_id}?collection=false", HttpMethod.get, False)
                if result[0] != 200:
                    logging.error(f"{result[0]}|{result[1]}")
                    await callback.answer("Произошла ошибка!", show_alert=True)
                    return
                form_of_study = result[1]
                object_id = form_of_study["form_of_study_id"]
            await get_qualifications(callback, object_id)
        case 3:
            await get_directions(callback, object_id)
        case 4:
            await get_direction(callback, object_id)
        # Добавить в закладки
        case 5:
            result = await send_request("/users/bookmarks", HttpMethod.post, True,
                                        {"user_id": callback.from_user.id, "direction_id": object_id})
            if result[0] != 200:
                logging.error(f"{result[0]}|{result[1]}")
                await callback.answer("Произошла ошибка!", show_alert=True)
                return
            logging.info(f'{callback.from_user.id}|{callback.from_user.full_name} - добавил в закладки направление {object_id}')
            await get_direction(callback, object_id)
        # Удалить из закладок
        case 6:
            result = await send_request("/users/bookmarks", HttpMethod.delete, True,
                                        {"user_id": callback.from_user.id, "direction_id": object_id})
            if result[0] != 200:
                logging.error(f"{result[0]}|{result[1]}")
                await callback.answer("Произошла ошибка!", show_alert=True)
                return
            logging.info(
                f'{callback.from_user.id}|{callback.from_user.full_name} - удалил из закладок направление {object_id}')
            await get_direction(callback, object_id)
