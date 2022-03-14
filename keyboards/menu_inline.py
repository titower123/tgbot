from aiogram.types import ReplyKeyboardRemove, \
    InlineKeyboardMarkup, InlineKeyboardButton

btn_1 = InlineKeyboardButton('Кнопка 1', callback_data='button1')
btn_2 = InlineKeyboardButton('Кнопка 2 ', callback_data='btn2')
inline_kb1 = InlineKeyboardMarkup(row_width=2).add(btn_1, btn_2)

btnt = InlineKeyboardButton('aboba', callback_data='aboba')
inline_kb2 = InlineKeyboardMarkup().add(btnt)