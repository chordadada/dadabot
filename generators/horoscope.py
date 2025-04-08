import aiohttp
from generators.chemical import generate_iupac_name

async def generate_horoscope(user_id: int) -> str:
    try:
        zodiac_signs = ["aries", "taurus", "gemini"]
        sign = zodiac_signs[user_id % len(zodiac_signs)]
        url = f"https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily?sign={sign}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                data = await response.json()
                prediction = data.get("data", {}).get("horoscope_data", "Звёзды молчат...")

    except Exception:
        prediction = "Сегодня звёзды предпочитают молчать. Создайте свой собственный хаос!"

    formula = generate_iupac_name()
    return (
        f"♓ Гороскоп для Дадаиста №{user_id % 1000}:\n"
        f"{prediction}\n\n"
        f"⚠️ Избегайте: {formula}"
    )
