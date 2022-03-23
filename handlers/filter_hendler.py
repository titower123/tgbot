from loader import dp
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.menu_inline import start_menu_cd

async def filter_EGE(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(text="Назад", callback_data=start_menu_cd.new(button_id="button_start"))
    )


    await call.message.edit_text("Пункт не готов :(", reply_markup=markup)