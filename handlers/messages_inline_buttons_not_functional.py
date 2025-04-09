from aiogram import Router, types, F
import random
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

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

# 🌌 Команда /horoscope — включает режим подписки с инлайн-кнопками «Да» в случайном виде
@router.message(F.text.startswith("/horoscope"))
async def cmd_horoscope(message: types.Message):
    user_id = message.from_user.id
    state = user_state.get_state(user_id)
    state["horoscope_mode"] = True
    state["horoscope_attempts"] = 0

    da_variants = ["Да", "да", "ДА", "дА", "𝔻𝔸", "ＤＡ", "🅳🅰", "🄳🄰"]
    button1 = random.choice(da_variants)
    button2 = random.choice([v for v in da_variants if v != button1])

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=button1, callback_data="subscribe_1"),
            InlineKeyboardButton(text=button2, callback_data="subscribe_2")
        ]
    ])

    await message.answer(
        "🌌 Готовы подписаться на гороскопы? Успех зависит от вашей квантовой неопределённости.",
        reply_markup=keyboard
    )


# ✅ Обработка callback-кнопок подписки
@router.callback_query(F.data.startswith("subscribe_"))
async def handle_inline_subscription(callback: CallbackQuery):
    user_id = callback.from_user.id
    state = user_state.get_state(user_id)

    if not state.get("horoscope_mode"):
        await callback.answer("Режим подписки неактивен.", show_alert=True)
        return

    attempts = state.get("horoscope_attempts", 0)
    success_chance = 0.33

    if random.random() < success_chance:
        add_to_mailing_list(user_id)
        state["horoscope_mode"] = False
        state["horoscope_attempts"] = 0
        await callback.message.edit_text(
            "✅ Подписка активирована. Гороскоп уже летит к вам сквозь туманность Ориона.",
            reply_markup=get_main_keyboard()
        )
    else:
        attempts += 1
        state["horoscope_attempts"] = attempts
        if attempts < 3:
            await callback.answer(f"❌ Неудача. Осталось попыток: {3 - attempts}", show_alert=True)
        else:
            state["horoscope_mode"] = False
            state["horoscope_attempts"] = 0
            await callback.message.edit_text(
                "❌ Космос отверг вашу просьбу. Подписка отменена.",
                reply_markup=get_main_keyboard()
            )


# ✅ Обычная кнопка «Да» (вне режима гороскопа)
@router.message(F.text == "Да")
async def handle_regular_da(message: types.Message):
    user_id = message.from_user.id
    state = user_state.get_state(user_id)

    if state.get("horoscope_mode"):
        await message.answer("🌀 Используйте инлайн-кнопки 'Да' под сообщением для подписки.")
        return

    await send_regular_response(message, state)
    collapse_chance = 0.1 + (state.get('banality_level', 0) * 0.02)
    if random.random() < collapse_chance:
        await trigger_quantum_collapse(message)
        state['banality_level'] = 0
    else:
        state['banality_level'] = state.get('banality_level', 0) + 1
    print(f"[{user_id}] Уровень абсурда: {state['banality_level']}")


@router.message()
async def handle_text(message: types.Message):
    user_id = message.from_user.id
    state = user_state.get_state(user_id)
    if state.get("horoscope_mode"):
        await message.answer("🔮 Подписка активна. Используйте кнопки 'Да' под сообщением.")
    else:
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
