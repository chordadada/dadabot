from aiogram import types
from utils.helpers import random_emojis

def get_main_keyboard(ghost_emoji: str = None) -> types.ReplyKeyboardMarkup:
    """
    Возвращает основную клавиатуру
    :param ghost_emoji: если None - кнопка-призрак не отображается
    """
    buttons = [
        [types.KeyboardButton(text="ДА"), types.KeyboardButton(text="НЕТ")],
        [],  # Здесь будут кнопки второй строки
        [types.KeyboardButton(text="Искусство"), types.KeyboardButton(text="Кот Шрёдингера")]
    ]
    
    # Добавляем кнопки во вторую строку
    buttons[1].extend([
        types.KeyboardButton(text=ghost_emoji) if ghost_emoji else None,
        types.KeyboardButton(text="Взрыв")
    ])
    
    # Фильтруем None (если ghost_emoji=None)
    buttons[1] = [btn for btn in buttons[1] if btn is not None]
    
    return types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
		
def get_ghost_emoji_variants() -> list[str]:
    """Возвращает все возможные варианты эмодзи для кнопки-призрака"""
    magic_emojis = [
        "👻", "🔮", "✨", "💫", "🌀", 
        "🌌", "🪄", "👀", "🌫️", "🫥"
    ]
    return magic_emojis