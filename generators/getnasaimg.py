import requests
import random
from datetime import datetime, timedelta
from config.settings import config

FALLBACK_IMAGES = [
    ("https://i.imgur.com/wgBhifK.jpeg", "Дадаистский коллаж (1920)"),
    ("https://i.imgur.com/M3NZpUA.jpeg", "Абстрактная композиция"),
    ("https://i.imgur.com/TUXzEH3.jpeg", "Революция форм")
]

async def get_nasa_eternal_image():
    """Получает космическое изображение с метафизическим описанием"""
    try:
        if not config.NASA_API_KEY:
            raise ValueError("NASA API ключ не найден")

        # Генерируем случайную дату за последние 25 лет
        random_date = datetime.now() - timedelta(days=random.randint(1, 25*365))
        
        params = {
            "api_key": config.NASA_API_KEY,
            "date": random_date.strftime("%Y-%m-%d"),
            "hd": True  # Максимальное качество
        }

        response = requests.get(
            "https://api.nasa.gov/planetary/apod",
            params=params,
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            if data["media_type"] != "image":
                return random.choice(FALLBACK_IMAGES)
            
            # Формируем "вечное" описание
            title = data.get("title", "Космическая бездна")
            explanation = data.get("explanation", "")
            
            eternal_phrases = [
                "Этот свет шёл к тебе миллионы лет",
                "Пыль взорвавшихся звёзд в твоих глазах",
                "Застывший момент вечности",
                "Свидетельство непостижимого"
            ]
            
            description = (
                f"🪐 {title}\n\n"
                f"{random.choice(eternal_phrases)}\n"
                f"▬▬▬\n"
                f"{explanation[:150]}..."  # Обрезаем до первого абзаца
            )

            return data["hdurl"], description

        return random.choice(FALLBACK_IMAGES)
    
    except Exception as e:
        print(f"NASA API error: {str(e)}")
        return random.choice(FALLBACK_IMAGES)