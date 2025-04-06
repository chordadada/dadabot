from aiogram import types
from utils.helpers import random_emojis
	
# def get_main_keyboard(force_da: bool = True) -> types.ReplyKeyboardMarkup:
    # buttons = [[
        # types.KeyboardButton(text="Да" if force_da else "Нет"), 
        # types.KeyboardButton(text="Да")
    # ]]
    # return types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
		
def get_main_keyboard(force_da: bool = True) -> types.ReplyKeyboardMarkup:
    left_text = "Да" if force_da else "Нет"
    buttons = [[types.KeyboardButton(text=left_text), types.KeyboardButton(text="Да")]]
    return types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
		
def get_ghost_emoji_variants() -> list[str]:
    """Возвращает все возможные варианты эмодзи для кнопки-призрака"""
    magic_emojis = [
        "👻", "🔮", "✨", "💫", "🌀", 
        "🌌", "🪄", "👀", "🌫️", "🫥"
    ]
    return magic_emojis