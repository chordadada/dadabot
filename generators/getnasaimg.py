import aiohttp
import random
from datetime import datetime, timedelta
from config.settings import config
import logging
logger = logging.getLogger(__name__)

FALLBACK_IMAGES = [
    ("https://i.imgur.com/wgBhifK.jpeg", "Дадаистский коллаж (1920)"),
    ("https://i.imgur.com/M3NZpUA.jpeg", "Абстрактная композиция"),
    ("https://i.imgur.com/TUXzEH3.jpeg", "Революция форм")
]

async def get_nasa_eternal_image():
    try:
        if not config.NASA_API_KEY:
            raise ValueError("NASA API ключ не найден")

        random_date = datetime.now() - timedelta(days=random.randint(1, 25 * 365))

        params = {
            "api_key": config.NASA_API_KEY,
            "date": random_date.strftime("%Y-%m-%d"),
            "hd": "True"
        }
        logger.debug(f"NASA Request Params: {params}")
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
            async with session.get("https://api.nasa.gov/planetary/apod", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("media_type") != "image":
                        return random.choice(FALLBACK_IMAGES)

                    gender = random.choice(phrases["genders"])
                    adj = random.choice(phrases["adjectives"][gender])
                    noun = random.choice(phrases["nouns"][gender])
                    template = random.choice(phrases["templates"][gender])
                    title = template.format(adj=adj, noun=noun)
                    description = f"{title}\n"

                    return data.get("hdurl") or data.get("url"), description

        return random.choice(FALLBACK_IMAGES)

    except Exception as e:
        logger.error(f"NASA API error: {str(e)}")
        return random.choice(FALLBACK_IMAGES)
