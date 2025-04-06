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
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import FSInputFile

# Создаём роутер
router = Router()
user_state = UserState()

# Новый обработчик кнопок "Да" с высоким приоритетом
@router.message(F.text == "Да", ~F.func(lambda msg: "horoscope_mode" in user_state.get_state(msg.from_user.id)))
async def handle_da_button(message: types.Message):
    user_id = message.from_user.id
    
    # Логика определения кнопки (левая=0, правая=1)
    keyboard = message.reply_markup.keyboard if message.reply_markup else None
    if keyboard and len(keyboard) > 0 and len(keyboard[0]) > 1:
        button_index = 0 if message.text == keyboard[0][0].text else 1
    else:
        button_index = random.randint(0, 1)
    
    # Проверка последовательности (распаковываем 3 значения)
    if user_id not in seq_gen.sequences:
        seq_gen.generate_sequence(user_id, length=random.randint(5, 5))
    
    target_seq, current_seq, _ = seq_gen.sequences.get(user_id, ("", "", 0.0))  # Добавлен timestamp
    
    is_correct = seq_gen.check_sequence(user_id, str(button_index))
    
    if current_seq == target_seq:
        await trigger_quantum_collapse(message)
        seq_gen.generate_sequence(user_id, length=random.randint(5, 5))
    elif not is_correct:
        seq_gen.sequences[user_id] = (target_seq, "", time.time())  # Сброс с timestamp
    print(f"User {user_id} input: {button_index}, Progress: {len(current_seq)}/{len(target_seq)}")
    return
				
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

@router.message(F.text == "Да", F.func(lambda msg: "horoscope_mode" in user_state.get_state(msg.from_user.id)))
async def handle_horoscope_input(message: types.Message):
    user_id = message.from_user.id
    state = user_state.get_state(user_id)
    
    if "horoscope_mode" not in state:
        return
    
    # Получаем текущую последовательность
    target_seq, current_seq, _ = seq_gen.sequences.get(user_id, ("", "", 0.0))
    
    # Определяем, какая кнопка считается правильной в текущем режиме
    current_mode = state["horoscope_mode"]
    is_right_button = current_mode % 2 == 0  # True если правая кнопка = "Да"
    
    # Проверяем нажатую кнопку (левая=0, правая=1)
    keyboard = message.reply_markup.keyboard
    button_index = 0 if message.text == keyboard[0][0].text else 1
    
    # Проверяем соответствие ожидаемому вводу
    expected_bit = "1" if is_right_button else "0"
    is_correct = (str(button_index) == expected_bit)
    
    if is_correct:
        # Обновляем текущую последовательность
        new_current_seq = current_seq + expected_bit
        seq_gen.sequences[user_id] = (target_seq, new_current_seq, time.time())
        
        # Проверяем завершение последовательности
        if new_current_seq == target_seq:
            add_to_mailing_list(user_id)
            await message.answer("🎉 Вы подписаны на гороскоп!")
            del state["horoscope_mode"]  # Завершаем процесс
        else:
            await message.answer("✓ Правильно! Продолжайте...")
    else:
        # Меняем режим кнопок и сбрасываем прогресс
        state["horoscope_mode"] += 1
        seq_gen.sequences[user_id] = (target_seq, "", time.time())
        
        # Обновляем клавиатуру для отображения изменений
        markup = get_main_keyboard(force_da=(current_mode % 2 == 1))
        hint = "Теперь левая кнопка = Да" if current_mode % 2 else "Теперь правая кнопка = Да"
        await message.answer(f"❌ Неверно! {hint}", reply_markup=markup)

# Модифицированный handle_message (убрана проверка на 👻 и коллапс)
@router.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    state = user_state.get_state(user_id)
    
    # Обновляем историю сообщений
    user_state.update_message_history(user_id, message.text)
    
    # Генерация обычного ответа (если не было коллапса)
    response = (
        f"{generate_thought()}\n\n"
        f"🧪 Катализатор: {generate_iupac_name()}\n"
        f"⚛️ Уровень абсурда: {state.get('banality_level', 0)}"
        f"\n{random_emojis(3)}"
    )
    await message.answer(response)
    
    # Обновление состояния
    state.update({
        'banality_level': state.get('banality_level', 0) + 1,
        'collapse_chance': state.get('collapse_chance', 0.1) + 0.05
    })
    
    # Логирование
    print(f"[{user_id}] Уровень: {state['banality_level']} | Шанс коллапса: {state['collapse_chance']:.2f}")
    print("═" * 50)