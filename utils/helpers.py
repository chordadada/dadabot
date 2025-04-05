# helpers.py
import random
from typing import Literal

EmojiSet = Literal["space", "science", "magic", "nature", "tech", "random"]

def random_emojis(
    count: int, 
    emoji_set: EmojiSet = "random",
    custom_emoji_list: list[str] | None = None
) -> str:
    """
    Генерирует строку со случайными эмодзи
    
    :param count: количество эмодзи
    :param emoji_set: predefined набор ("space", "science", "magic", etc.)
    :param custom_emoji_list: свой собственный список эмодзи для выбора
    :return: строка со случайными эмодзи
    """
    emoji_banks = {
        "space": ["🌀", "⚛️", "💫", "🌌", "🔭", "🛸", "👾", "🌠", "🚀", "👽"],
        "science": ["🧪", "🔬", "⚗️", "🧫", "🧬", "🧮", "🔭", "📡", "🧲", "⚙️"],
        "magic": ["🔮", "✨", "🎩", "🪄", "💫", "👻", "🎭", "🕯️", "🌙", "♾️"],
        "nature": ["🌿", "🌸", "🌻", "🍄", "🌳", "🌊", "☀️", "🌈", "❄️", "⚡"],
        "tech": ["💻", "📱", "🖥️", "⌨️", "🖱️", "📡", "🔋", "💾", "🖲️", "📲"],
        "random": ["🌀", "⚛️", "💫", "🌌", "🔭", "🧪", "💥", "🔮", "🌪️", "👾"]
    }
    
    bank = custom_emoji_list or emoji_banks.get(emoji_set, emoji_banks["random"])
    return ''.join(random.choices(bank, k=count))

