from generators.getnasaimg import get_nasa_eternal_image
from generators.getwikimg import get_random_wiki_image

async def get_image(user_progress: float):
    if user_progress > 0.5:
        return await get_nasa_eternal_image()
    else:
        return await get_random_wiki_image()