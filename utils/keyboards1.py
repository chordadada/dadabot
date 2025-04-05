from aiogram import types

def get_main_keyboard():
    buttons = [
        ["ДА", "НЕТ"],
        ["👻", "Взрыв"],
        ["Искусство", "Кот Шрёдингера"]
    ]
    return types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=btn) for btn in row] for row in buttons],
        resize_keyboard=True
    )