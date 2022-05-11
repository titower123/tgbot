from loader import dp
from aiogram import types, utils
from data.config import ADMINS
from utils.db_api.db_commands.db_commands_new_user import get_all_new_users


@dp.message_handler(commands='show_new_users')
async def show_new_users(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        users = ""
        await message.answer(text='Отправляю список пользователей')
        list_users = await get_all_new_users()
        for user in list_users:
            users += f'Дата добавления: {user.date_and_time}\nИмя пользователя: {user.full_name}\n' \
                     f'ID пользователя:{user.user_id}\n\n '
        if len(users) > 4096:
            for i in range(0, len(users), 4096):
                await message.answer(text=users[i:i + 4096])
        else:
            await message.answer(text=users)
