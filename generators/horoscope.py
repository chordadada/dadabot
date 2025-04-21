import aiohttp
import random
from generators.chemical import generate_iupac_name
from utils.helpers import random_emojis, dadamizer
from aiogram.utils.text_decorations import html_decoration as hd
from generators.translator import translator

async def generate_horoscope(user_id: int) -> str:
    try:
        zodiac_signs = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"]
        sign = random.choice(zodiac_signs)
        url = f"https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily?sign={sign}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                data = await response.json()
                prediction_draft = data.get("data", {}).get("horoscope_data", "Звёзды молчат...")
                prediction = await translator.quantum_translate(prediction_draft, depth=3)

    except Exception:
        prediction = "Сегодня звёзды предпочитают молчать. Создайте свой собственный хаос!"

    formula = generate_iupac_name()
    today = random.choice([" судьбы", " дня", " дна", " знай", ", нах", ""])
    emoset = random.choice(["space", "science", "magic", "nature", "tech", "random"])		
    return (
        f"<b>🔮 Дадаскоп для Дадаиста №{(user_id % 10000)**2}</b>\n\n"
        f"🌪 Знаки{today}: <tg-spoiler>{' '.join(random_emojis(5, emoset))}</tg-spoiler>\n\n"
        f"<b>📜 Расшифровка:</b>\n{(dadamizer(text=prediction, chaos_level=1))}\n\n"
        f"⚠️ <b>ИЗБЕГАЙТЕ:</b>\n<code>{hd.quote(formula)}</code>\n\n"
        f"🌀 <i>Уровень хаоса: {random.randint(1, 100)}%</i>"
    )