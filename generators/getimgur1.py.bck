import requests
import random
from config.settings import config

async def get_random_imgur_image():
    """Получает случайное изображение с Imgur"""
    try:
        if not config.IMGUR_CLIENT_ID:
            return None, "Ключ доступа к галерее утерян в квантовом пространстве"
            
        headers = {"Authorization": f"Client-ID {config.IMGUR_CLIENT_ID}"}
        response = requests.get(
            "https://api.imgur.com/3/gallery/search/top/week?q=dadaism",
						#f"https://api.imgur.com/3/gallery/search/top/week?q=dada&page={random.randint(0, 10)}",
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        
        # Фильтруем только изображения
        posts = [
            post for post in response.json()["data"] 
            if not post.get("is_album") 
            and post["link"].lower().endswith(('.jpg', '.png', '.jpeg'))
        ]
        
        if not posts:
            return None, "Галерея дадаизма пуста. Создайте что-то новое!"
            
        chosen = random.choice(posts)
        return chosen["link"], chosen.get("title", "Безымянный шедевр")
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка Imgur API: {str(e)}")
        return None, "Галерея временно закрыта на дезинфекцию "
    except Exception as e:
        print(f"Неожиданная ошибка: {str(e)}")
        return None, "Искусство сопротивляется категоризации"