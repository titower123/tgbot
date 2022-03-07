from aiogram.types import Message
from loader import dp

@dp.message_handler(state=None)
async def hello(message: Message):
    {
        await message.answer(f'Ты написал {message.text}')
    }