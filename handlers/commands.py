from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from states.user_states import UserState
from generators.visual import generate_pseudoscience_chart
from generators.text import generate_thought
from generators.chemical import generate_iupac_name
from utils.keyboards import get_main_keyboard, get_ghost_emoji_variants
from utils.helpers import random_emojis
from aiogram.types import FSInputFile
from aiogram.filters import Command
from utils.decorators import log_activity
import random
import asyncio

router = Router()
user_state = UserState()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
		# Получаем случайный эмодзи для кнопки
    ghost_emoji = random_emojis(1, emoji_set="magic")
    # Создаём клавиатуру (всегда показываем кнопку при /start)
    markup = get_main_keyboard(ghost_emoji=ghost_emoji)
    await message.answer("Вы согласны с тем, что ничего не согласны?", reply_markup=markup)
    print(f"🌀 Пользователь {message.from_user.id} начал квантовый диалог")
		
@router.message(F.text == "Кот Шрёдингера")
async def quantum_cat(message: types.Message):
    state = random.choice(["жив", "мёртв"])
    markup = get_main_keyboard()
    await message.answer(f"Кот {state}!\n...но это не точно", 
                        reply_markup=markup)
    # Логируем событие
    user_state.get_state(message.from_user.id)["quantum_events"] += 1

@router.message(F.text == "Взрыв")
async def explosion(message: types.Message):
    for i in range(5, 0, -1):
        await message.answer(f"{i}...")
        await asyncio.sleep(1)
    await message.answer("💥 *тишина*")
    await asyncio.sleep(3)
    await message.answer("Сюрприз! Взрыв был метафорой.")

@router.message(F.text == "Искусство")
async def send_art(message: types.Message):
    media = random.choice([
        "https://i.imgur.com/FmtgAhR.jpeg",
        "https://i.imgur.com/Fj8tDx4.png"
    ])
    if media.endswith(".mp4"):
        await message.answer_video(media)
    else:
        await message.answer_photo(media)
    await message.answer("Это стоило 1.2 миллиона евро. Вы не понимаете.")

@router.message(F.text.in_(get_ghost_emoji_variants()))
async def ghost_button(message: types.Message):
    # 30% шанс полного исчезновения
    if random.random() < 0.3:
        await message.answer(
            f"{message.text} растворился в квантовой пене!",
            reply_markup=types.ReplyKeyboardRemove()
        )
        return
    
    # 50% шанс что кнопка изменится, 50% что исчезнет
    if random.random() < 0.5:
        new_emoji = random_emojis(1, emoji_set="magic")
        markup = get_main_keyboard(ghost_emoji=new_emoji)
        await message.answer(f"Кнопка превратилась в {new_emoji}!", reply_markup=markup)
    else:
        markup = get_main_keyboard(ghost_emoji=None)  # Без кнопки-призрака
        await message.answer("Кнопка исчезла... но ненадолго!", reply_markup=markup)
				
@router.message(F.text == "Поговори сам с собой")
async def self_chat(message: types.Message):
    for _ in range(3):
        await message.answer(generate_thought())
        await asyncio.sleep(1)
    await message.answer("Диалог окончен. Вы проиграли.")
		
@router.message(Command("help"))
@log_activity
async def cmd_help(message: types.Message):
    help_text = (
        "🌀 <b>Руководство по квантовому безумию:</b>\n\n"
        "→ /chaos — Активировать случайную функцию\n"
        "→ /horoscope — Предсказание из антиматерии\n"
        "→ /feedback — Отправить сообщение в никуда\n"
        "→ /antimanual — Самоуничтожающаяся инструкция\n"
        "→ /help — Этот список безумия\n\n"
        "→ @бот_юзернейм — Инлайн-режим абсурда\n\n"
        "<i>Просто пиши что угодно — система коллапсирует!</i>"
    )
    await message.answer(help_text, parse_mode="HTML")
		
@router.message(Command("antimanual"))
@log_activity
async def cmd_antimanual(message: types.Message):
    await message.answer(
        "📜 *Инструкция уничтожена.*\n"
        f"Причина: {generate_iupac_name()}\n"
        "Попробуйте /help для новой версии"
    )
		
@router.message(Command("chaos"))
@log_activity 
async def cmd_chaos(message: types.Message, state: FSMContext):
    # Обработчик с дополнительными параметрами
    await state.update_data(chaos_level=10)
    await message.answer("Хаос активирован!")