import requests
import random
from config.settings import config

async def get_random_imgur_image():
    """Улучшенный запрос с диагностикой"""
    try:
        # 1. Проверка ключа
        if not config.IMGUR_CLIENT_ID:
            print("Ошибка: IMGUR_CLIENT_ID не установлен")
            return None, "Ключ галереи утерян в квантовом вакууме"
        
        # 2. Формируем запрос
        headers = {"Authorization": f"Client-ID {config.IMGUR_CLIENT_ID}"}
        queries = [
            "dadaism",
            "abstract art",
            "surrealism",
            "experimental art"
        ]
        
        # 3. Пробуем разные запросы
        for query in queries:
            try:
                response = requests.get(
                    f"https://api.imgur.com/3/gallery/search/top/week?q={query}",
                    headers=headers,
                    timeout=15
                )
                response.raise_for_status()
                
                data = response.json()
                posts = [
                    post for post in data.get("data", [])
                    if not post.get("is_album", True)
                    and post.get("link", "")
                    and not post.get("nsfw", True)
                ]
                
                if posts:
                    chosen = random.choice(posts)
                    print(f"Успешный запрос по тегу: {query}")
                    return chosen["link"], chosen.get("title", "Безымянный артефакт")
                    
            except Exception as e:
                print(f"Ошибка при запросе по тегу '{query}': {str(e)}")
                continue
                
        # 4. Если ничего не найдено
        print("Все запросы вернули пустой результат")
        return None, "Галерея требует вашего вмешательства. Создайте новый шедевр!"
        
    except Exception as e:
        print(f"Критическая ошибка в get_random_imgur_image: {str(e)}")
        return None, "Квантовый сбой в системе искусств"