import aiohttp
import random
import logging
logger = logging.getLogger(__name__)

FALLBACK_IMAGES = [
    ("https://i.imgur.com/wgBhifK.jpeg", "Дадаистский коллаж (1920)"),
    ("https://i.imgur.com/M3NZpUA.jpeg", "Абстрактная композиция"),
    ("https://i.imgur.com/TUXzEH3.jpeg", "Революция форм")
]

async def get_random_wiki_image():
    try:
        params = {
            "action": "query",
            "generator": "categorymembers",
            "gcmtitle": "Category:Art",
            "gcmlimit": 50,
            "prop": "imageinfo",
            "iiprop": "url|extmetadata",
            "iiurlwidth": 800,
            "format": "json"
        }

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
            async with session.get("https://commons.wikimedia.org/w/api.php", params=params) as response:
                if response.status != 200:
                    return random.choice(FALLBACK_IMAGES)

                data = await response.json()
                pages = data.get("query", {}).get("pages", {}).values()

                valid_images = [
                    p for p in pages
                    if "imageinfo" in p
                    and "CC" in p["imageinfo"][0].get("extmetadata", {}).get("LicenseShortName", {}).get("value", "")
                ]

                if not valid_images:
                    return random.choice(FALLBACK_IMAGES)

                chosen = random.choice(valid_images)
                image_info = chosen["imageinfo"][0]
                original_url = image_info["url"]

                title = f"{random.choice(['Трансцендентное', 'Кашемировое', 'Ржавое'])} {random.choice(['изваяние', 'фиаско', 'семя знахарки'])}"
                art_phrases = [
                    "Непорочное, как само искусство",
                    "Шокарует ли? Отнюдь!",
                    "Бокал игристого!",
                    "Печаль и боль — вот мой пароль"
                ]
                description = f"{title}\n\n{random.choice(art_phrases)}\n"

                return original_url, description

    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")
        return random.choice(FALLBACK_IMAGES)
