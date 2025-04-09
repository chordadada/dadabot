from aiogram import Router, types, F
import asyncio
import random
from aiogram.types import FSInputFile

from generators.chemical import generate_iupac_name
from generators.text import generate_thought
from generators.visual import generate_pseudoscience_chart
from states.user_states import UserState
from utils.helpers import random_emojis
from utils.decorators import log_activity
from utils.database import add_to_mailing_list
from states.user_states import user_state

router = Router()
#user_state = UserState()

@router.message(F.text == "Да")
async def handle_da(message: types.Message):
    user_id = message.from_user.id
    state = user_state.get_state(user_id)

    # Если активирован режим подписки на гороскоп
    if state.get("horoscope_mode"):
        attempts = state.get("horoscope_attempts", 0)
        success_chance = 0.33  # вероятность успеха подписки

        if random.random() < success_chance:
            add_to_mailing_list(user_id)
            state["horoscope_mode"] = False
            state["horoscope_attempts"] = 0
            await message.answer("✅ Вы успешно подписались на квантовые гороскопы! 🌌")
        else:
            attempts += 1
            state["horoscope_attempts"] = attempts
            if attempts < 3:
                await message.answer(f"❌ Подписка не удалась. Осталось попыток: {3 - attempts}")
            else:
                state["horoscope_mode"] = False
                state["horoscope_attempts"] = 0
                await message.answer("❌ Подписка не удалась. Режим гороскопа отключён.")
        return  # Завершаем обработку, чтобы не обрабатывать как обычное сообщение

    # Если бот не в режиме подписки – обрабатываем как обычное сообщение
    await send_regular_response(message, state)

    # Логика квантового коллапса
    collapse_chance = 0.1 + (state.get('banality_level', 0) * 0.02)
    if random.random() < collapse_chance:
        await trigger_quantum_collapse(message)
        state['banality_level'] = 0
    else:
        state['banality_level'] = state.get('banality_level', 0) + 1

    print(f"[{user_id}] Уровень абсурда: {state['banality_level']}")

# Обработчик для всех сообщений, кроме тех, где текст равен "Да"
@router.message(lambda message: message.text != "Да")
async def handle_text(message: types.Message):
    user_id = message.from_user.id
    state = user_state.get_state(user_id)
    if state.get("horoscope_mode"):
        await message.answer("🌀 Сейчас активна квантовая подписка на гороскоп. Нажмите «Да».")
        return
    await message.answer("🌀 Только кнопки 'Да' имеют силу в этом измерении!")

async def send_regular_response(message: types.Message, state: dict):
    response = (
        f"{generate_thought()}\n"
        f"🧪 Реактив: {generate_iupac_name()}\n"
        f"⚛️ Уровень абсурда: {state.get('banality_level', 0)}\n"
        f"{random_emojis(3)}"
    )
    await message.answer(response)

async def trigger_quantum_collapse(message: types.Message):
    user_id = message.from_user.id
    chart_path = generate_pseudoscience_chart(user_id)
    await message.answer_photo(FSInputFile(chart_path))
    emojis = random_emojis(5, emoji_set="space")
    await message.answer(f"🌀 Квантовый коллапс! {emojis}")
    user_state.get_state(user_id).update({
        'collapse_chance': 0.1,
        'banality_level': 0
    })
