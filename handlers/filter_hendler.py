from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.filter_inline import filter_direction_keyboard, filter_directions_keyboard, main_keyboard, filter_cd, \
    direction_cd
from loader import dp
from states.filter_state import Filter_class
from utils.db_api.db_commands.db_commands_hendler import get_all_str, get_direction
from states.filter_state import user_request


# начальное сообщение
async def filter_ege(call: types.CallbackQuery):
    markup = await main_keyboard()
    await call.message.edit_text("Выберите до 4-х предметов.", reply_markup=markup)


# обработчик первого нажатия
@dp.callback_query_handler(filter_cd.filter())
async def answer_1(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    subject_id = callback_data["subject_id"]
    if subject_id == 'Найти':
        await call.message.answer(text='Извините, вы не выбрали <b>ни одного предмета</b>. Повторите еще раз.')
    else:
        await state.update_data(answer1=subject_id)
        await call.answer(f"Вы выбрали {subject_id}")
        await Filter_class.first()


# обработчик второго нажатия
@dp.callback_query_handler(filter_cd.filter(), state=Filter_class.subject1)
async def answer_2(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    subject_id = callback_data["subject_id"]
    if subject_id == 'Найти':
        data = await state.get_data()
        data_ = list(data.values())
        await state.finish()
        await find(call, data_)
    else:
        await state.update_data(answer2=subject_id)
        await call.answer(f"Вы выбрали {subject_id}")
        await Filter_class.next()


# обработчик третьего нажатия
@dp.callback_query_handler(filter_cd.filter(), state=Filter_class.subject2)
async def answer_3(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    subject_id = callback_data["subject_id"]
    if subject_id == 'Найти':
        data = await state.get_data()
        data_ = list(data.values())
        await state.finish()
        await find(call, data_)
    else:
        await state.update_data(answer3=subject_id)
        await call.answer(f"Вы выбрали {subject_id}")
        await Filter_class.next()


# обработчик четвертого нажатия
@dp.callback_query_handler(filter_cd.filter(), state=Filter_class.subject3)
async def answer_4(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    subject_id = callback_data["subject_id"]
    if subject_id == 'Найти':
        data = await state.get_data()
        data_ = list(data.values())
        await state.finish()
        await find(call, data_)
    else:
        # await call.answer(f"Вы выбрали {subject_id}")
        await state.update_data(answer4=subject_id)
        data = await state.get_data()
        data_ = list(data.values())
        await state.finish()
        await find(call, data_)


async def find(callback: types.CallbackQuery, prefix):
    all_data = await get_all_str()
    l_data_ = len(prefix)
    element_count = 0
    list_directions = []
    for el in all_data:
        count = 0
        if el.exams != None:
            item = el.exams.split('|')
            for i in range(l_data_):
                if item.count(prefix[i]) == 1:
                    count += 1
            if count == l_data_:
                list_directions.append(el.id)
                element_count += 1
    if element_count == 0:
        await callback.answer(
            f'Извините, по вашему запросу ({", ".join(prefix)}) я не смог найти ни одного направления.',
            show_alert=True)
    else:
        #записаьб str_list_direction в список юзер : значение str_list_direction
        user_request[callback.from_user.id] = list_directions
        await callback.answer(f'Ваш запрос: {" ".join(prefix)}', show_alert=True)
        await list_directions_level(callback, callback.from_user.id)


async def list_directions_level(callback: types.CallbackQuery, user_id, direction_id=None):
    markup = await filter_directions_keyboard(user_id=user_id)
    await callback.message.edit_text(text='Направления по вашему запросу', reply_markup=markup)


async def list_direction_level(callback: types.CallbackQuery, list_directions_user_id, direction_id):
    markup = await filter_direction_keyboard(user_id=str(list_directions_user_id), direction_id=direction_id)
    direction = await get_direction(direction_id)
    text = f"""<b>{direction.name}</b>\n\n{str(direction.description)}"""
    await callback.message.edit_text(text=text, reply_markup=markup)


# обработчик запроса по предмету
@dp.callback_query_handler(direction_cd.filter())
async def navigete_directions(call: types.CallbackQuery, callback_data: dict):
    current_level = callback_data.get('level')
    user_id = callback_data.get('user_id')
    direction_id = int(callback_data.get('direction_id'))

    levels = {
        '1': list_directions_level,
        '2': list_direction_level
    }

    func_cur_level = levels[current_level]
    await func_cur_level(
        call,
        user_id,
        direction_id
    )
