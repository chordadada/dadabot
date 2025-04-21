import random
from typing import Literal
from datetime import timedelta

def format_cooldown(seconds: int) -> str:
    """Форматирует время в ЧЧ:ММ:СС"""
    return str(timedelta(seconds=seconds)).split(".")[0]

EmojiSet = Literal["space", "science", "magic", "nature", "tech", "random"]

def dadamizer(text: str, chaos_level: int = 1) -> str:
    """
    Искажает текст в дадаистическом стиле с HTML-форматированием.
    
    :param text: исходный текст
    :param chaos_level: уровень хаоса (1-5)
    :return: модифицированный текст с эмодзи и форматированием
    """
    words = text.split()
    modified = []
    chaos_prob = chaos_level * 0.15
    
    for i, word in enumerate(words):
        # HTML-форматирование
        if random.random() < chaos_prob:
            formats = [
                lambda x: f"<b>{x}</b>",    # Жирный
                lambda x: f"<i>{x}</i>",    # Курсив
                lambda x: f"<s>{x}</s>",    # Зачёркнутый
                lambda x: x.upper(),        # ВЕРХНИЙ РЕГИСТР
                lambda x: x[::-1],          # Перевёрнутое
            ]
            word = random.choice(formats)(word)
        
        # Случайные символы (без угловых скобок)
        if random.random() < chaos_prob/2:
            additions = [
                random.choice(["⁂", "※", "⁑"]),
                random.choice(["•", "◦", "‣"])
            ]
            word = random.choice(additions) + word if i%2 == 0 else word + random.choice(additions)
        
        modified.append(word)
    
    # Вставка эмодзи
    emoji_count = min(chaos_level + 1, 5)
    emojis = random_emojis(emoji_count, emoji_set=random.choice([EmojiSet]), allow_duplicates=True)
    
    # Собираем результат
    result = []
    for i, word in enumerate(modified):
        result.append(word)
        if random.random() < chaos_prob * 0.7:
            result.append(random.choice(emojis.split()))
    
    return ' '.join(result)

def random_emojis(
    count: int, 
    emoji_set: EmojiSet = "random",
		allow_duplicates: bool = False,
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
    if allow_duplicates:
        return ' '.join(random.choices(bank, k=count))
    return ' '.join(random.sample(bank, min(count, len(bank))))