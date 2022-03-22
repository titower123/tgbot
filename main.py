from asyncore import dispatcher
from aiogram import executor

from utils.set_default_commands import set_default_commands
from utils.notify_admins import on_startup_notify
from utils.notify_admins import shutdown_bot
from utils.db_api.database import create_db

async def on_starup(dispatcher):
	await set_default_commands(dispatcher)
	await on_startup_notify(dispatcher)
	await create_db()
async def on_shutdown(dispatcher):
	await shutdown_bot(dispatcher)


if __name__ == "__main__":
	from handlers import dp
	executor.start_polling(dp, on_startup=on_starup, on_shutdown=on_shutdown)



