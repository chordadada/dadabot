import requests
from datetime import datetime
from generators.chemical import generate_iupac_name

async def generate_horoscope(user_id: int) -> str:
    try:
        # Пример API (можно заменить на любое бесплатное)
        zodiac_signs = ["aries", "taurus", "gemini"]
        sign = zodiac_signs[user_id % 3]
        response = requests.get(f"https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily?sign={sign}")
        prediction = response.json()["data"]["horoscope_data"]
    except:
        prediction = "Сегодня звёзды предпочитают молчать. Создайте свой собственный хаос!"

    formula = generate_iupac_name()
    return (
        f"♓ Гороскоп для Дадаиста №{user_id % 1000}:\n"
        f"{prediction}\n\n"
        f"⚠️ Избегайте: {formula}"
    )
		
# async def generate_horoscope(user_id: int) -> str:
    # try:
        Альтернативный API на случай ошибок
        # zodiacs = ["aries", "taurus", "gemini", "cancer", "leo"]
        # sign = random.choice(zodiacs)  # Больше вариантов
        # url = f"https://ohmanda.com/api/horoscope/{sign}/"
        # response = requests.get(url, timeout=10)
        # prediction = response.json().get("horoscope", "Звёзды безмолвствуют. Создайте свой хаос!")
    
    # except Exception as e:
        # prediction = f"Оракул в отпуске. Ошибка: {str(e)}"

    # return (
        # f"♓ Квантовый прогноз №{user_id % 1000}:\n{prediction}\n\n"
        # f"☣️ Избегайте: {generate_iupac_name()}"
    # )