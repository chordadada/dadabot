from aiogram import Bot, Router, types, F
from aiogram.fsm.context import FSMContext
from states.user_states import UserState
#from states.user_states import UserStates
from generators.visual import generate_pseudoscience_chart
from generators.text import generate_thought
from generators.chemical import generate_iupac_name
from generators.getwikimg import get_random_wiki_image
from generators.getnasaimg import get_nasa_eternal_image
from generators.casgen import cas_gen
import requests
from datetime import datetime
from utils.database import add_to_mailing_list
from generators.image_provider import get_image
from utils.keyboards import get_main_keyboard
from utils.helpers import random_emojis, dadamizer, format_cooldown
from aiogram.types import FSInputFile
from aiogram.filters import Command
from utils.decorators import log_activity
import random
import asyncio
import time
from datetime import timedelta
from random import choice
from core.bot_instance import get_bot
from states.user_states import user_state, feedback_state
#from aiogram.enums import ParseMode
import logging
logger = logging.getLogger(__name__)

#Список для ботфазера
# start - Пси и Хи
# dadart - Порция из куста
# dadascope - Предсказание из антиматери
# dadascope_daily - Подписка на Дадаскоп
# dadafuturism - Пальпация прошлого
# dadaphone - Отправить сообщение в никуда
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
  
@router.message(Command("dadascope_daily"))
async def cmd_horoscope(message: types.Message):
    user_id = message.from_user.id
    state = user_state.get_state(user_id)
    state["horoscope_mode"] = True
    state["horoscope_attempts"] = 0  # Сброс счетчика попыток
    await message.answer(
        "🌀 Нажмите 'Да' чтобы квантово подписаться на дадаскопы!\n"
        "Успех не гарантирован!",
        reply_markup=get_main_keyboard()
    )

async def send_daily_horoscope():
    """Ежедневная рассылка дадаскопов подписчикам"""
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
            logger.info(f"✓ дадаскоп отправлен для {user_id}")
            
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
            f"<b>{random_emojis(1)} {title}</b>\n"
            f"{random_emojis(1)} Оценочная стоимость: {random.randint(1, 10000000)} евро\n"
            f"{random_emojis(1)} Комментарий критикессы: <i>{generate_thought(author = False)}</i>"
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
        f"{random_emojis(1)} <b>Руководство по хордададаизации:</b>\n\n"
        "→ /start - Начать дадалог\n"
        "→ /dadart - Получить дадъект\n"
        "→ /dadascope - Прозреть дадаскоп\n"
        "→ /dadascope_daily - Подписаться на\n"
        "→ /dadafuturism - Хрустальный сосут\n"
        "→ /dadaphone - Квантовый дадаводчик\n"
        "→ /help - Хэлп\n\n"
        "<i>Просто пиши ДаДа — система дадапсирует!</i>"
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
                f"Мнение Человечицы: {verdict}\n\n"
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
        
@router.message(Command("dadafuturism"))
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
    
@router.message(Command("dadascope"))
async def dadascope_handler(message: types.Message):
    user_id = message.from_user.id
    state = user_state.get_state(user_id)
    current_time = time.time()
    
    if state.get('last_dadascope') and (current_time - state['last_dadascope'] < 86400):
        remaining = 86400 - (current_time - state['last_dadascope'])
        await message.answer(
            f"{random_emojis(1)} Дадагмат перезаряжается!\n"
            f"До следующего дадаскопа: {format_cooldown(int(remaining))}"
        )
        return
    
    state['last_dadascope'] = current_time
    await send_daily_horoscope()
    logger.info(f"Дадаскоп отправлен пользователю {user_id}")
    
@router.message(Command("dadaphone"))
@log_activity
async def start_quantum_dialog(message: types.Message, state: FSMContext):
    await state.set_state(feedback_state.quantum_feedback)
    await state.update_data(translation_depth=1)
    await message.answer(
        f"{random_emojis(1)} Дада у дадафона. Что у вас на уме?\n"
        f"Ответим не медленно и не быстро, а может и не ответим. Да."
    )

@router.message(Command("cas"))
@log_activity
async def cmd_cas(message: types.Message):
    try:
        response = await cas_gen.generate_cas_info()
        await message.answer(response)
    except Exception as e:
        logger.error(f"CAS error: {str(e)}")
        await message.answer("🌀 Реактив самоуничтожился!")