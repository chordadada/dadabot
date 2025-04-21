from aiogram import Router, types, F
import asyncio
import random
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from generators.chemical import generate_iupac_name
from generators.text import generate_thought
from generators.visual import generate_pseudoscience_chart
from states.user_states import UserState
from utils.helpers import random_emojis, dadamizer
from utils.decorators import log_activity
from utils.database import add_to_mailing_list
from states.user_states import user_state, feedback_state
from utils.keyboards import DA_VARIANTS, get_main_keyboard
from generators.translator import translator
#from states.user_states import UserStates

import logging
logger = logging.getLogger(__name__)

router = Router()
#user_state = UserState()

@router.message(feedback_state.quantum_feedback)
async def handle_quantum_feedback(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    depth = user_data.get('translation_depth', 1)
    
    translated_d = await translator.quantum_translate(message.text, depth)
    translated = dadamizer(translated_d, chaos_level=2)
    await message.answer(f"{translated}", parse_mode="HTML")
    
    if depth >= translator.max_depth:
        await message.answer(
              "⚠️ Хлипкая нить понимания оборвалась!\n"
              "Обращайтесь по адресу: г. Минск, ул. К. Маркса, 38.\n"
              "Успехов и в добрый путь! 🚨", reply_markup=get_main_keyboard()
          )
        await state.clear()
    else:
        await state.update_data(translation_depth=depth + 1)

@router.message(F.text.in_(DA_VARIANTS))
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
            await message.answer("✅ Вы успешно подписались на квантовые гороскопы! 🌌",
            reply_markup=get_main_keyboard())
        else:
            attempts += 1
            state["horoscope_attempts"] = attempts
            if attempts < 3:
                await message.answer(f"❌ Подписка не удалась. Осталось попыток: {3 - attempts}",
                reply_markup=get_main_keyboard())
            else:
                state["horoscope_mode"] = False
                state["horoscope_attempts"] = 0
                await message.answer("❌ Подписка не удалась. Режим гороскопа отключён.",
                reply_markup=get_main_keyboard())
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

    logger.info(f"[{user_id}] Уровень абсурда: {state['banality_level']}")
    
# Обработчик для всех сообщений, кроме вариаций "Да"
@router.message(~F.text.in_(DA_VARIANTS))
async def handle_text(message: types.Message):
    user_id = message.from_user.id
    state = user_state.get_state(user_id)
    if state.get("horoscope_mode"):
        await message.answer("🌀 Сейчас активна квантовая подписка на гороскоп. Используйте кнопки 'ДАДА'.",
        reply_markup=get_main_keyboard())
        return
    await message.answer("🌀 Всегда говори ДаДа!",
    reply_markup=get_main_keyboard())

async def send_regular_response(message: types.Message, state: dict):
    user_progress = random.random()
    if user_progress > 0.75:
        response = (
        f"{random.choice(["Заруби себе на носу!", "Напутствие на сегодня:", "Дадаист, Помни!", "Дружок-старичок передаёт:", "Важно знать!"])}\n"
        f"{dadamizer(generate_thought(), chaos_level = 3)}\n"
        f"ДАДА подтекст: {random_emojis(random.randint(1, 10))}\n"
    )
    else:
        response = " ".join(dadamizer(random.choice(DA_VARIANTS), chaos_level=4) for _ in range(random.randint(1, 7)))
    await message.answer(response, reply_markup=get_main_keyboard())

async def trigger_quantum_collapse(message: types.Message):
    user_id = message.from_user.id
    chart_path = generate_pseudoscience_chart(user_id)
    emojis = random_emojis(5, emoji_set="space")
    await message.answer_photo(FSInputFile(chart_path),
    f"🌀 Квантовый коллапс! {emojis}", reply_markup=get_main_keyboard())
    user_state.get_state(user_id).update({
        'collapse_chance': 0.1,
        'banality_level': 0
    })
