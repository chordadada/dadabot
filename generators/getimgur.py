import requests
import random
from config.settings import config

# Список гарантированных изображений на случай пустого ответа API
FALLBACK_IMAGES = [
    ("https://i.imgur.com/wgBhifK.jpeg", "Дадаистский коллаж (1920)"),
    ("https://i.imgur.com/M3NZpUA.jpeg", "Абстрактная композиция"),
    ("https://i.imgur.com/TUXzEH3.jpeg", "Революция форм")
]

async def get_random_imgur_image():
    """Получает изображение, используя API или fallback-коллекцию"""
    try:
        if config.IMGUR_CLIENT_ID:
            headers = {"Authorization": f"Client-ID {config.IMGUR_CLIENT_ID}"}
            queries = [
                "art", 
                "photography",
                "retro"
            ]
            
            for query in queries:
                try:
                    response = requests.get(
                        f"https://api.imgur.com/3/gallery/search/top/week?q={query}",
                        headers=headers,
                        timeout=10
                    )
                    if response.status_code == 200:
                        posts = [
                            p for p in response.json().get("data", [])
                            if not p.get("is_album") 
                            and p.get("link", "").split(".")[-1].lower() in ["jpg", "png", "jpeg"]
                        ]
                        if posts:
                            chosen = random.choice(posts)
                            return chosen["link"], chosen.get("title", f"Анонимное произведение ({query})")
                except Exception as e:
                    print(f"Ошибка при запросе '{query}': {str(e)}")
                    continue
    
    except Exception as e:
        print(f"Общая ошибка: {str(e)}")
    
    # Возвращаем fallback-изображение если API не сработало
    return random.choice(FALLBACK_IMAGES)