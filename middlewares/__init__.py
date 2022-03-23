from aiogram import Dispatcher


from .throttling import ThrottlingMiddleware
from .support_middleware import SupportMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(SupportMiddleware())
