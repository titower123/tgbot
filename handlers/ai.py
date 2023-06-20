from loader import dp
from aiogram import types
from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters.state import StatesGroup, State
from utils.network_tools import send_request_to_ai
from keyboards.start_keyboard import home_markup


ai_cb = CallbackData("ai", "action")

class AiState(StatesGroup):
    question = State()


async def wait_message_form_user(callback: types.CallbackQuery):
    await callback.message.edit_text("Отправь сообщение с вопросом", reply_markup=home_markup())
    await AiState.question.set()


@dp.message_handler(state=AiState.question)
async def answer_from_ai(message: types.Message):
    question = message.text
    result = ''
    try:
        result = await send_request_to_ai({"q": [question]})
        answer = result[0][0]
        await message.answer(answer, reply_markup=home_markup())
    except:
        await message.answer("Я сейчас не могу ответить :(", reply_markup=home_markup())


@dp.callback_query_handler(ai_cb.filter())
async def ai_callback_controller(callback: types.CallbackQuery, callback_data:dict):
    action = callback_data['action']
    match action:
        case "start":
            await wait_message_form_user(callback)
