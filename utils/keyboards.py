from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from utils.helpers import random_emojis
import random

DA_VARIANTS = ["Da", "DA", "da", "Да", "да", "ДА", "дА", "𝔻𝔸", "ＤＡ", "🅳🅰", "🄳🄰"]

def get_main_keyboard() -> ReplyKeyboardMarkup:
    # Выбираем два уникальных варианта
    variants = random.sample(DA_VARIANTS, 2)
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=variants[0]), KeyboardButton(text=variants[1])]],
        resize_keyboard=True,
        one_time_keyboard=False
    )

def get_horoscope_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="ДАДА")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )