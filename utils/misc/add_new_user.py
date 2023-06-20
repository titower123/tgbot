from datetime import datetime

from loader import dp
from utils.misc.notify_admins import notify_new_user_add


async def add_new_users(message):
    # if await find_user(message.from_user.id):
    #     print(f'|{datetime.now().strftime("%d/%m/%Y - %H:%M:%S")}| Новый пользователь - {message.from_user.id},'
    #           f' {message.from_user.full_name}')
    #     await notify_new_user_add(dp=dp, user_id=message.from_user.id, full_name=message.from_user.full_name)
    #     await add_user(user_id=message.from_user.id, full_name=message.from_user.full_name)
    pass