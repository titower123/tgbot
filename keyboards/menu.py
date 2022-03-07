from cgitb import text
from tkinter import Button
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Фильтр"),
            KeyboardButton(text="Дерево")
        ],
        [
            KeyboardButton(text="Документы для поступления")
        ],
    ],
    resize_keyboard=True
)