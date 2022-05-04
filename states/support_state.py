from aiogram.dispatcher.filters.state import StatesGroup, State


class SupportClass(StatesGroup):
    answer = State()