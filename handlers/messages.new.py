from aiogram import Router, types, F
import random
from aiogram.types import FSInputFile

from generators.chemical import generate_iupac_name
from generators.text import generate_thought
from generators.visual import generate_pseudoscience_chart
from states.user_states import UserState
from utils.helpers import random_emojis
from utils.database import add_to_mailing_list
from utils.keyboards import get_main_keyboard
from states.user_states import user_state


router = Router()
#user_state = UserState()

# 🔮 Обработка кнопки ДАДА в режиме подписки
@router.message(F.text == "ДАДА")
async def handle_dada_subscription(message: types.Message):
    user_id = message.from_user.id
    state = user_state.get_state(user_id)

    if not state.get("horoscope_mode"):
        await message.answer("🌀 Эта кнопка доступна только в режиме гороскопа.")
        return

    attempts = state.get("horoscope_attempts", 0)
    success_chance = 0.33

    if random.random() < success_chance:
        add_to_mailing_list(user_id)
        state["horoscope_mode"] = False
        state["horoscope_attempts"] = 0
        await message.answer(
            "✅ Подписка активирована. Гороскоп уже летит к вам сквозь туманность Ориона.",
            reply_markup=get_main_keyboard()
        )
    else:
        attempts += 1
        state["horoscope_attempts"] = attempts
        if attempts < 3:
            await message.answer(
                f"🚫 Подписка не удалась. Попробуйте ещё раз. Осталось попыток: {3 - attempts}"
            )
        else:
            state["horoscope_mode"] = False
            state["horoscope_attempts"] = 0
            await message.answer(
                "❌ Космос отверг вашу просьбу. Подписка отменена.",
                reply_markup=get_main_keyboard()
            )

# ✅ Обычная кнопка «Да» (вне режима гороскопа)
@router.message(F.text == "Да")
async def handle_regular_da(message: types.Message):
    user_id = message.from_user.id
    state = user_state.get_state(user_id)

    # Если пользователь случайно нажал Да в режиме гороскопа
    if state.get("horoscope_mode"):
        await message.answer("🌀 Вы в режиме гороскопа. Используйте кнопку «ДАДА».")
        return

    await send_regular_response(message, state)

    # Квантовый коллапс
    collapse_chance = 0.1 + (state.get('banality_level', 0) * 0.02)
    if random.random() < collapse_chance:
        await trigger_quantum_collapse(message)
        state['banality_level'] = 0
    else:
        state['banality_level'] = state.get('banality_level', 0) + 1

    print(f"[{user_id}] Уровень абсурда: {state['banality_level']}")

# ❌ Все остальные сообщения
@router.message()
async def handle_text(message: types.Message):
    user_id = message.from_user.id
    state = user_state.get_state(user_id)

    if state.get("horoscope_mode"):
        await message.answer("🌠 Сейчас активна подписка на гороскоп. Нажмите «ДАДА».")
    else:
        await message.answer("🌀 Только кнопки 'Да' имеют силу в этом измерении!")

# 🔁 Ответ вне режима
async def send_regular_response(message: types.Message, state: dict):
    response = (
        f"{generate_thought()}\n"
        f"🧪 Реактив: {generate_iupac_name()}\n"
        f"⚛️ Уровень абсурда: {state.get('banality_level', 0)}\n"
        f"{random_emojis(3)}"
    )
    await message.answer(response)

# 💥 Квантовый коллапс
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
