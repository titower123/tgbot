from aiogram import executor
from utils.misc.set_default_commands import set_default_commands
from utils.misc.notify_admins import on_startup_notify
from utils.misc.notify_admins import shutdown_bot
from utils.misc.examination import examination
from utils.network_tools import get_token, stop_timer
from utils.network_tools import get_users
import logging


async def on_startup(dispatcher):
    import middlewares
    try:
        get_token()
    except Exception as e:
        logging.error(e)
    await get_users()
    examination()
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)
    middlewares.setup(dp)


async def on_shutdown(dispatcher):
    await shutdown_bot(dispatcher)
    stop_timer()



# TODO: переделать строение проекта, т.к есть баги с глобальными переменами
if __name__ == "__main__":
    from handlers import dp
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
