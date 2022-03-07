from cgitb import text
from distutils import command
from email import message
from email.message import Message
from pyexpat.errors import messages
import telebot
from telebot import types

bot = telebot.TeleBot("1851983410:AAErHp8ZMMyBXKGNTIFCToaDIX9k-2Njp88", parse_mode=None)

start_message_text =  """
Привет, я помогу тебе определиться с выбором.
Внизу есть кнопки.
"""

start_markup = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('Фильтр по ЕГЭ')
itembtn2 = types.KeyboardButton('Поиск специальности')
itembtn3 = types.KeyboardButton('Документы для поступления')
start_markup.add(itembtn1, itembtn2, itembtn3)


@bot.message_handler(commands=['start'])
def start_message(user):
	{
		bot.send_message(chat_id=user.chat.id, text=start_message_text, reply_markup=start_markup)
	}

bot.infinity_polling()
