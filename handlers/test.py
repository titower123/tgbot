from pkgutil import get_data
from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp
from states.test import Test
from aiogram.dispatcher import FSMContext

@dp.message_handler(Command('test'), state=None)
async def test(message: types.Message):
    await message.answer("Начинаю проверку на морду.\n"
    "Первый вопрос. Вы морда?")
    await Test.Q1.set()

@dp.message_handler(state=Test.Q1)
async def answerQ1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(
        {"answer1": answer}
    )
    await message.answer("Второй вопрос: Вы уверены что вы не морда?")

    await Test.Q2.set()

@dp.message_handler(state=Test.Q2)
async def answerQ2(message: types.Message, state: FSMContext):
    answer2 = message.text
    data = await state.get_data()
    answer1 = data.get("answer1")

    await message.answer(f"Вы морда\n"
    f"Ваши ответы:\nПервый вопрос: {answer1}\nВторой вопрос: {answer2}"
    )
    await state.finish()
