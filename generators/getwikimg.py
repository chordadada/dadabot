import requests
import random
from urllib.parse import quote_plus
from config.settings import config

# Список гарантированных изображений на случай пустого ответа API
FALLBACK_IMAGES = [
    ("https://i.imgur.com/wgBhifK.jpeg", "Дадаистский коллаж (1920)"),
    ("https://i.imgur.com/M3NZpUA.jpeg", "Абстрактная композиция"),
    ("https://i.imgur.com/TUXzEH3.jpeg", "Революция форм")
]

async def get_random_wiki_image():
    """Получает случайное изображение из Wikimedia Commons"""
    try:
        # Параметры запроса для поиска в категории "Art"
        params = {
            "action": "query",
            "generator": "categorymembers",
            "gcmtitle": "Category:Art",  # Можно изменить категорию
            "gcmlimit": 50,
            "prop": "imageinfo",
            "iiprop": "url|extmetadata",
            "iiurlwidth": 800,  # Ширина превью
            "format": "json"
        }

        response = requests.get(
            "https://commons.wikimedia.org/w/api.php",
            params=params,
            timeout=15
        )

        if response.status_code != 200:
            return random.choice(FALLBACK_IMAGES)

        data = response.json()
        pages = data.get("query", {}).get("pages", {}).values()

        # Фильтрация только изображений с лицензией
        valid_images = [
            p for p in pages 
            if "imageinfo" in p 
            and "CC" in p["imageinfo"][0].get("extmetadata", {}).get("LicenseShortName", {}).get("value", "")
        ]

        if not valid_images:
            return random.choice(FALLBACK_IMAGES)

        chosen = random.choice(valid_images)
        image_info = chosen["imageinfo"][0]
        
        # Извлечение данных
        image_url = image_info["thumburl"]  # Превью
        original_url = image_info["url"]    # Оригинал
        
        # Формирование описания с атрибуцией
        metadata = image_info["extmetadata"]
        author = metadata.get("Artist", {}).get("value", "Неизвестный автор")
        title = metadata.get("ObjectName", {}).get("value", "Без названия")
        license = metadata.get("LicenseShortName", {}).get("value", "CC-BY-SA")

        #description = f"{title} (Автор: {author}, Лицензия: {license})"
				
        adjectives = ["Трансцендентное", "Кашемировое", "Ржавое"]
        nouns = ["изваяние", "фиаско", "семя знахарки"]
        title = f"{random.choice(adjectives)} {random.choice(nouns)}"
        explanation = data.get("explanation", "")
        
        art_phrases = [
            "Непорочное, как само искусство",
            "Шокарует ли? Отнюдь!",
            "Бокал игристого!",
            "Печаль и боль — вот мой пароль"
        ]

        description = (
            f"{title}\n\n"
            f"{random.choice(art_phrases)}\n"
        )

        return original_url, description

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        return random.choice(FALLBACK_IMAGES)