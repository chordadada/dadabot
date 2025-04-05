from aiogram import types
import random

def get_main_keyboard(ghost_emoji: str = "👻", include_ghost: bool = True) -> types.ReplyKeyboardMarkup:
    """Возвращает основную клавиатуру с динамической кнопкой-призраком"""
    ghost_emojis = ["👻", "👀", "💨", "🌀", "✨", "🌫️", "🫥"]
    chosen_emoji = ghost_emoji if ghost_emoji in ghost_emojis else random.choice(ghost_emojis)
    
    base_buttons = [
        ["ДА", "НЕТ"],
        ["Взрыв"],
        ["Искусство", "Кот Шрёдингера"]
    ]
    
    # Добавляем кнопку-призрак только если include_ghost=True
    if include_ghost:
        base_buttons[1].insert(0, chosen_emoji)  # Вставляем в начало второй строки
    
    return types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=btn) for btn in row] for row in base_buttons],
        resize_keyboard=True,
        selective=True  # Показывать клавиатуру только активным пользователям
    )

def get_ghost_emoji_variants() -> list[str]:
    """Возвращает список возможных эмодзи для кнопки-призрака"""
    return ["👻", "👀", "💨", "🌀", "✨", "🌫️", "🫥"]