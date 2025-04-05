from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
import random
import asyncio
from enum import Enum

bot = Bot(
    token="7741399072:AAHahbxExHlXm72LwgtDyPM719YqvTii9MQ",
    default=DefaultBotProperties(parse_mode="HTML")
)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Списки сообщений
pseudo_wisdom = [
    "Согласно квантовой термодинамике, {user}, ваш чайник наблюдает за вами через {chem}.",
    "Фрактальный алгоритм {chem} доказывает, что вы — случайная ошибка в матрице."
]

chemicals = ["дигидрогена монооксид", "C₈H₁₀N₄O₂ (кофеин)"]

absurd_media = [
    "https://i.imgur.com/FmtgAhR.jpeg",
    "https://i.imgur.com/Fj8tDx4.png"   # Кот в костюме Наполеона
]

# Глобальная переменная
message_counter = 0

class QuantumState(Enum):
    CAT_ALIVE = 1
    CAT_DEAD = 2

# Обработчик команды /start
@dp.message(F.text == "/start")
async def start(message: types.Message):
    keyboard = [
        [types.KeyboardButton(text="ДА"), types.KeyboardButton(text="НЕТ")],
        [types.KeyboardButton(text="👻"), types.KeyboardButton(text="Взрыв")],
        [types.KeyboardButton(text="Искусство"), types.KeyboardButton(text="Кот Шрёдингера")]
    ]
    markup = types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    await message.answer("Вы согласны с тем, что ничего не согласны?", reply_markup=markup)

# Исчезающая кнопка
@dp.message(F.text == "👻")
async def ghost_button(message: types.Message):
    await message.answer("Кнопки не было. Тебе показалось.")
    await message.answer("...или нет?", reply_markup=types.ReplyKeyboardRemove())
    
# Обработчик всех сообщений
@dp.message()
async def reply(message: types.Message):
    global message_counter
    message_counter += 1
    
    response = random.choice(pseudo_wisdom).format(
        user=message.from_user.first_name,
        chem=random.choice(chemicals)
    )
    await message.answer(response)
    
    if random.random() < 0.2:
        response = response.translate(str.maketrans('абвгд', 'ϥѝґґђ'))  # Искажение текста
        await message.answer(response + "\n\nПеревод: ЭТО НЕВАЖНО")
    
    if message_counter % 5 == 0:
        await message.answer("ЭТО УЖЕ БЫЛО. ПРЕКРАТИ.")
        await message.answer(response)  # Повтор предыдущего сообщения

@dp.message(F.text == "Кот Шрёдингера")
async def quantum_cat(message: types.Message):
    state = random.choice(list(QuantumState))
    await message.answer(f"Кот {'жив' if state == QuantumState.CAT_ALIVE else 'мёртв'}")
    await message.answer("...но это не точно", reply_markup=types.ReplyKeyboardRemove())
    
@dp.message(F.text == "Взрыв")
async def explosion(message: types.Message):
    for i in range(5, 0, -1):
        await message.answer(f"{i}...")
        await asyncio.sleep(1)
    await message.answer("💥 *тишина*")
    await asyncio.sleep(3)
    await message.answer("Сюрприз! Взрыв был метафорой.")
    
@dp.message(F.text == "Искусство")
async def send_art(message: types.Message):
    media = random.choice(absurd_media)
    if media.endswith(".mp4"):
        await message.answer_video(media)
    else:
        await message.answer_photo(media)
    await message.answer("Это стоило 1.2 миллиона евро. Вы не понимаете.")
    
@dp.message(F.text == "Поговори сам с собой")
async def self_chat(message: types.Message):
    for _ in range(3):
        await message.answer(random.choice(pseudo_wisdom))
        await asyncio.sleep(1)
    await message.answer("Диалог окончен. Вы проиграли.")

if __name__ == '__main__':
    dp.run_polling(bot)