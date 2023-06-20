import logging
from datetime import datetime
import aiogram.utils.exceptions
from loader import dp
from aiogram import types
from keyboards.filter_keyboard import filter_direction_keyboard, filter_directions_keyboard, main_keyboard, filter_cd, \
    direction_cd
from utils.network_tools import send_request, HttpMethod
from core.strings import START_MESSAGE, ANSWER_1_ERROR, DEF_FIND_ERROR_MESSAGE, DEF_LIST_DIRECTIONS_LEVEL
from .manual_search import message_text

# список с предметами пользователя (ключ: id пользователя, значение: предметы)
list_user_prefix = {}


# начальное сообщение
async def filter_ege(call: types.CallbackQuery):
    if call.from_user.id in list_user_prefix.keys():
        list_user_prefix.pop(call.from_user.id)
    await call.message.edit_text(text=START_MESSAGE, reply_markup=main_keyboard())


# обработчик первого нажатия
@dp.callback_query_handler(filter_cd.filter())
async def answer_1(call: types.CallbackQuery, callback_data: dict):
    subject_id = callback_data["subject_id"]
    if subject_id == 'Сброс':
        try:
            await filter_ege(call)
            return
        except Exception as ex:
            return
    if subject_id == 'Найти':
        if call.from_user.id not in list_user_prefix.keys():
            await call.answer(text=ANSWER_1_ERROR, show_alert=True)
            try:
                await filter_ege(call)
            except Exception:
                return
        else:
            await find(call, list_user_prefix[call.from_user.id])
    else:
        if call.from_user.id not in list_user_prefix.keys():
            list_user_prefix[call.from_user.id] = [subject_id]
            await call.message.edit_text(text=f'Вы выбрали: {subject_id}', reply_markup=main_keyboard())
            return
        if subject_id in list_user_prefix[call.from_user.id]:
            await call.answer(text=f'Вы уже выбрали {subject_id}', show_alert=True)
            return
        list_user_prefix[call.from_user.id].append(subject_id)
        await call.message.edit_text(text=f'Вы выбрали: {", ".join(list_user_prefix[call.from_user.id])}',
                                     reply_markup=main_keyboard())


async def find(callback: types.CallbackQuery, prefix):
    print(f'|{datetime.now().strftime("%d/%m/%Y - %H:%M:%S")}|{callback.from_user.id},'
          f' {callback.from_user.full_name}|{prefix}|- запрос пользователя в фильтре')
    list_user_prefix[callback.from_user.id] = prefix
    await list_directions_level(callback)


async def list_directions_level(callback: types.CallbackQuery):
    prefix = []
    try:
        prefix = list_user_prefix[callback.from_user.id]
    except Exception as e:
        await filter_ege(callback)
        print(f'|{datetime.now().strftime("%d/%m/%Y - %H:%M:%S")}|{callback.from_user.id},'
              f' {callback.from_user.full_name}|{e, e.args}|- ошибка в фильтре')
        return
    result = await send_request("/filter", HttpMethod.post, False, json={"directions": prefix})
    if result[0] != 200:
        logging.error(f"{result[0]}|{result[1]}")
        await callback.answer("Произошла ошибка!", show_alert=True)
        return
    resultJson = result[1]
    if len(resultJson) == 0:
        try:
            print(f'|{datetime.now().strftime("%d/%m/%Y - %H:%M:%S")}|{callback.from_user.id},'
                  f' {callback.from_user.full_name} - не удачный запрос {prefix}')
            await callback.answer(DEF_FIND_ERROR_MESSAGE.format(", ".join(prefix)), show_alert=True)
        except aiogram.utils.exceptions.BadRequest as exce:
            print(
                f'|{datetime.now().strftime("%d/%m/%Y - %H:%M:%S")}|{callback.from_user.id},'
                f' {callback.from_user.full_name} - ошибка в запросе {exce}')
            await callback.answer(text='Извините, по вашему запросу я не смог ничего найти', show_alert=True)
        await filter_ege(call=callback)
        return
    try:
        markup = await filter_directions_keyboard(user_id=callback.from_user.id, directions=resultJson)
        print(f'|{datetime.now().strftime("%d/%m/%Y - %H:%M:%S")}|{callback.from_user.id},'
              f' {callback.from_user.full_name}|- смотрит направления по запросу')
        await callback.message.edit_text(DEF_LIST_DIRECTIONS_LEVEL.format(", ".join(prefix), len(resultJson)),
                                         reply_markup=markup)
    except Exception as ex:
        await filter_ege(callback)
        print(f'|{datetime.now().strftime("%d/%m/%Y - %H:%M:%S")}|{callback.from_user.id},'
              f' {callback.from_user.full_name}|{ex, ex.args}|- ошибка в фильтре')
        return


async def list_direction_level(callback: types.CallbackQuery, direction_id):
    result = await send_request(f"/directions/{direction_id}", HttpMethod.get, False)
    if result[0] != 200:
        logging.error(f"{result[0]}|{result[1]}")
        await callback.answer("Произошла ошибка!", show_alert=True)
        return
    resultJson = result[1]
    markup = await filter_direction_keyboard(user_id=callback.from_user.id, direction_id=resultJson["id"])
    print(f'|{datetime.now().strftime("%d/%m/%Y - %H:%M:%S")}|{callback.from_user.id},'
          f' {callback.from_user.full_name}|{direction_id}|- смотрит направление по запросу')
    await callback.message.edit_text(text=message_text(resultJson), reply_markup=markup)
    pass


# обработчик запроса по предмету
@dp.callback_query_handler(direction_cd.filter())
async def navigate_directions(call: types.CallbackQuery, callback_data: dict):
    current_level = int(callback_data['level'])
    direction_id = str(callback_data['direction_id'])
    match current_level:
        case 1:
            await list_directions_level(call)
        case 2:
            await list_direction_level(call, direction_id)
        case 3:
            result = await send_request("/users/bookmarks", HttpMethod.post, True,
                                        {"user_id": call.from_user.id, "direction_id": direction_id})
            if result[0] != 200:
                logging.error(f"{result[0]}|{result[1]}")
                await call.answer("Произошла ошибка!", show_alert=True)
                return
            await list_direction_level(call, direction_id)
        case 4:
            result = await send_request("/users/bookmarks", HttpMethod.delete, True,
                                        {"user_id": call.from_user.id, "direction_id": direction_id})
            if result[0] != 200:
                logging.error(f"{result[0]}|{result[1]}")
                await call.answer("Произошла ошибка!", show_alert=True)
                return
            await list_direction_level(call, direction_id)
