import random
import json
import logging

logger = logging.getLogger(__name__)

def generate_thought():
    try:
        with open('data/phrases.json', 'r', encoding='utf-8') as f:
            phrases = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Файл phrases.json не найден или повреждён: {e}")
        phrases = {}

    # Резервные значения для всех ключей
    default_phrases = {
        'intro': ['Внезапно обнаружилось'],
        'noun': ['неклассифицируемый объект'],
        'verb': ['модифицирует'],
        'concept': ['вашу квантовую суперпозицию'],
        'quote': ['«Безумие — это норма»'],
        'author': ['Анонимный диссидент'],
        'absurd_comment': ['Зачем вы это читаете?']
    }

    # Автозаполнение отсутствующих ключей
    for key in default_phrases:
        if key not in phrases:
            logger.warning(f"⚠️ Ключ '{key}' отсутствует, используются резервные значения")
            phrases[key] = default_phrases[key]

    # Генерация структуры мысли
    try:
        structure = random.choice([
            ["intro", "noun", "verb", "concept"],
            ["quote", "author", "absurd_comment"]
        ])
        return ' '.join([random.choice(phrases[key]) for key in structure])
    except Exception as e:
        logger.error(f"💥 Критическая ошибка: {e}")
        return "Мысль исчезла в сингулярности"
		
    logger.info(f"Сгенерирована мысль для {user_id}: {result[:50]}...")