from aiogram import Router, types, F
from generators.chemical import generate_iupac_name
from generators.text import generate_thought
from generators import seq_gen
from generators.sequencer import SequenceGenerator
from generators.visual import generate_pseudoscience_chart
from states.user_states import UserState
from utils.helpers import random_emojis
from utils.decorators import log_activity
from utils.database import add_to_mailing_list
from aiogram.types import FSInputFile
import time
import random
import asyncio
import logging
logger = logging.getLogger(__name__)

# Создаём роутер
router = Router()
user_state = UserState()

@router.message(F.text == "Да")
async def handle_da(message: types.Message):
    user_id = message.from_user.id
    state = user_state.get_state(user_id)

    if state.get("horoscope_mode"):
        # Принудительный сброс
        state["horoscope_mode"] = False
        
        if random.random() < 0.33:
            add_to_mailing_list(user_id)
            await message.answer("✅ Активирован поток предсказаний!")
            logger.info(f"🌀 Новый подписчик: {user_id}")
        else:
            await message.answer("❌ Связь с будущим потеряна!")
        
        return

    # Обычный режим
    await send_regular_response(message, state)
    
    # Логика коллапса (10% базовый шанс + 2% за уровень)
    collapse_chance = 0.1 + (state.get('banality_level', 0) * 0.02)
    if random.random() < collapse_chance:
        await trigger_quantum_collapse(message)
        state['banality_level'] = 0
    else:
        state['banality_level'] = state.get('banality_level', 0) + 1

    logger.info(f"[{user_id}] Уровень абсурда: {state['banality_level']}")

async def send_regular_response(message: types.Message, state: dict):
    response = (
        f"{generate_thought()}\n"
        f"🧪 Реактив: {generate_iupac_name()}\n"
        f"⚛️ Уровень абсурда: {state['banality_level']}\n"
        f"{random_emojis(3)}"
    )
    await message.answer(response)


async def trigger_quantum_collapse(message: types.Message):
    user_id = message.from_user.id
    
    # Генерация психоделического графика
    chart_path = generate_pseudoscience_chart(user_id)
    await message.answer_photo(FSInputFile(chart_path))
    
    # Рандомные эмодзи и сообщение
    emojis = random_emojis(5, emoji_set="space")
    await message.answer(f"🌀 Квантовый коллапс! {emojis}")
    
    # Сброс состояния
    user_state.get_state(user_id).update({
        'collapse_chance': 0.1,
        'banality_level': 0
    })
		
@router.message()
async def handle_text(message: types.Message):
    await message.answer("🌀 Только кнопки 'Да' имеют силу в этом измерении!")