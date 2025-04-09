import random
from typing import List
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from generators.unicode_generator import get_cached_variants

# Инициализация при старте бота
DA_VARIANTS = get_cached_variants() + ["ＤＡ", "𝔻𝔸", "🅳🅰", "🄳🄰" ]

def get_main_keyboard() -> ReplyKeyboardMarkup:
    variants = random.sample(DA_VARIANTS, k=2)
    buttons = [[KeyboardButton(text=variants[0]), KeyboardButton(text=variants[1])]]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=False
    )

