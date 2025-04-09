from aiogram import Bot, Router, types, F
from aiogram.fsm.context import FSMContext
from states.user_states import UserState
from generators.visual import generate_pseudoscience_chart
from generators.text import generate_thought
from generators.chemical import generate_iupac_name
from generators.getwikimg import get_random_wiki_image
from generators.getnasaimg import get_nasa_eternal_image
import requests
from datetime import datetime
from utils.database import add_to_mailing_list
from generators.image_provider import get_image
from utils.keyboards import get_main_keyboard
from utils.helpers import random_emojis
from aiogram.types import FSInputFile
from aiogram.filters import Command
from utils.decorators import log_activity
import random
import asyncio
from random import choice
from core.bot_instance import get_bot
from states.user_states import user_state
#from aiogram.enums import ParseMode
import logging
logger = logging.getLogger(__name__)

#Список для ботфазера
# start - Пси и Хи
# dadart - Порция из куста
# eternaldada - Вечное сияние дада
# horoscope - Предсказание из антиматери
# feedback - Отправить сообщение в никуда
# antimanual - Самоуничтожающаяся инструкция
# help - Зачем это всё

router = Router()
#user_state = UserState()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer("Вы согласны с тем, что ничего не согласны?", reply_markup=get_main_keyboard())
    logger.info(f"🌀 Пользователь {message.from_user.id} начал квантовый диалог")
		
@router.message(F.text == "Кот Шрёдингера")
async def quantum_cat(message: types.Message):
    state = random.choice(["жив", "мёртв"])
    await message.answer(f"Кот {state}!\n...но это не точно", 
                        reply_markup=get_main_keyboard())
    # Логируем событие
    user_state.get_state(message.from_user.id)["quantum_events"] += 1

@router.message(F.text == "Взрыв")
async def explosion(message: types.Message):
    for i in range(5, 0, -1):
        await message.answer(f"{i}...")
        await asyncio.sleep(1)
    await message.answer("💥 *тишина*")
    await asyncio.sleep(3)
    await message.answer("Сюрприз! Взрыв был метафорой.", reply_markup=get_main_keyboard())
	
@router.message(Command("horoscope"))
async def cmd_horoscope(message: types.Message):
    user_id = message.from_user.id
    state = user_state.get_state(user_id)
    state["horoscope_mode"] = True
    state["horoscope_attempts"] = 0  # Сброс счетчика попыток
    await message.answer(
        "🌀 Нажмите 'Да' чтобы квантово подписаться на гороскопы!\n"
        "Успех не гарантирован!",
        reply_markup=get_main_keyboard()
    )

async def send_daily_horoscope():
    """Ежедневная рассылка гороскопов подписчикам"""
    from core.bot_instance import get_bot
    from utils.database import mailing_list
    from generators.horoscope import generate_horoscope
    
    bot = get_bot()
    
    for user_id in list(mailing_list):  # Создаем копию для безопасной итерации
        try:
            # 1. Проверяем доступность чата
            await bot.get_chat(user_id)  # Вызовет исключение если бот заблокирован
            
            # 2. Генерируем контент
            text = await generate_horoscope(user_id)
            
            # 3. Отправляем сообщение
            await bot.send_message(
                chat_id=user_id,
                text=text,
                disable_notification=True,  # Тихая отправка
								parse_mode="HTML"
            )
            logger.info(f"✓ Гороскоп отправлен для {user_id}")
            
        except Exception as e:
            logger.error(f"✕ Ошибка для {user_id}: {str(e)}")
            mailing_list.discard(user_id)  # Удаляем недоступных пользователей
            continue  # Переходим к следующему

@router.message(Command("dadart"))
async def send_art(message: types.Message):
    try:
        user_progress = random.random()
        media_url, title = await get_image(user_progress)
        if not media_url:
            await message.answer(title)
            return

        caption = (
            f"<b>🌀 {title}</b>\n"
            f"💶 Оценочная стоимость: {random.randint(1000, 1000000)} евро\n"
            f"📰 Комментарий критикессы: <i>{generate_thought()}</i>"
        )

        if media_url.endswith(('.mp4', '.webm', '.gifv', '.gif')):
            await message.answer_animation(
                media_url,
                caption=caption[:1024],  # Ограничение Telegram на 1024 символа
								parse_mode="HTML",
								reply_markup=get_main_keyboard()
            )
        else:
            await message.answer_photo(
                media_url,
                caption=caption[:1024],
								parse_mode="HTML",
								reply_markup=get_main_keyboard()
            )

    except Exception as e:
        await message.answer("Арт-объект самоуничтожился при передаче 🕳️", reply_markup=get_main_keyboard())
        logger.error(f"Ошибка отправки: {str(e)}", exc_info=True)
	
@router.message(F.text == "Поговори сам с собой")
async def self_chat(message: types.Message):
    for _ in range(3):
        await message.answer(generate_thought())
        await asyncio.sleep(1)
    await message.answer("Диалог окончен. Вы проиграли.", reply_markup=get_main_keyboard())
		
@router.message(Command("help"))
@log_activity
async def cmd_help(message: types.Message):
    help_text = (
        "🌀 <b>Руководство по квантовому безумию:</b>\n\n"
        "→ /start - Начать диалог\n"
        "→ /dadart - Получить арт-объект\n"
        "→ /horoscope - Гороскоп-провокация\n"
        "→ /futuredada - Видео из будущего\n"
        "→ /feedback - Квантовый переводчик\n\n"
        "<i>Просто пиши что угодно — система коллапсирует!</i>"
        )
    await message.answer(help_text, parse_mode="HTML", reply_markup=get_main_keyboard())
		
@router.message(Command("eternaldada"))
@log_activity
async def send_cosmic_dada(message: types.Message):
    # Получаем космический артефакт
    media_url, cosmic_description = await get_nasa_eternal_image()
    
    # Генерируем абсурдные мета-данные
    price = random.choice(["♾ кг звёздной пыли", f"{random.randint(1,100)} чёрных дыр"])
    verdict = random.choice([
        "Этот объект отрицает само понятие искусства",
        "Галактический совет признал работу нелегитимной",
        "Квантовая пена в восторге"
    ])

    try:
        # Отправляем медиа с дада-интерпретацией
        if media_url.endswith(('.mp4', '.webm')):
            await message.answer_video(media_url, caption=cosmic_description[:1024], reply_markup=get_main_keyboard())
        else:
            await message.answer_photo(
                media_url,
                f"⚡ АРТ-РЕЛИКТ №{random.randint(10**12, 10**18)}\n\n"
                f"Оценочная стоимость: {price}\n"
                f"Вердикт Совета Бессмертных: {verdict}\n\n"
                f"<tg-spoiler>📜 {cosmic_description}</tg-spoiler>",
								reply_markup=get_main_keyboard()
            )

    except Exception as e:
        # Фолбэк с концептуальным объяснением
        await message.answer(
            "Космический вакуум поглотил артефакт\n\n"
            "▫️▫️▫️▫️▫️▫️▫️▫️\n"
            "Это и есть высшая форма искусства",
						reply_markup=get_main_keyboard()
        )
        logger.error(f"Квантовая ошибка: {str(e)}")
				
@router.message(Command("futuredada"))
async def send_future_dada(message: types.Message):
    videos = [
        "https://t.me/chordadada/123",
        "https://t.me/chordadada/456"
    ]
    caption = random.choice([
        "Вот, что тебя ждёт!",
        "Берегись этого!",
        "Твоё будущее уже здесь!"
    ])
    await message.answer_video(random.choice(videos), caption=caption)
		
# Временный код для теста (добавить в commands.py)
@router.message(Command("test_horoscope"))
async def test_send(message: types.Message):
    await send_daily_horoscope()