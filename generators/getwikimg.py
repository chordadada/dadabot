import aiohttp
import random
import logging
import json
logger = logging.getLogger(__name__)

FALLBACK_IMAGES = [
    ("https://i.imgur.com/wgBhifK.jpeg", "Дадаистский коллаж (1920)"),
    ("https://i.imgur.com/M3NZpUA.jpeg", "Абстрактная композиция"),
    ("https://i.imgur.com/TUXzEH3.jpeg", "Революция форм")
]

try:
    with open('data/phrases.json', 'r', encoding='utf-8') as f:
        phrases = json.load(f)
except FileNotFoundError:
    raise Exception("Файл phrases.json не найден в папке data!")

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

                gender = random.choice(phrases["genders"])
                adj = random.choice(phrases["adjectives"][gender])
                noun = random.choice(phrases["nouns"][gender])
                template = random.choice(phrases["templates"][gender])
                title = template.format(adj=adj, noun=noun)
                description = f"{title}\n"

                return original_url, description

    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")
        return random.choice(FALLBACK_IMAGES)
