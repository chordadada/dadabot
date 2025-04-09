from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from utils.helpers import random_emojis
	
def get_main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Да"), KeyboardButton(text="Да")]],
        resize_keyboard=True,
        one_time_keyboard=False
    )
		
def get_horoscope_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="ДАДА")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
