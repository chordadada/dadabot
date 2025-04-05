from aiogram import Router, types, F
from generators.chemical import generate_iupac_name
from generators.text import generate_thought
from generators.visual import generate_pseudoscience_chart
from states.user_states import UserState
from utils.helpers import random_emojis
from utils.decorators import log_activity
from aiogram.types import FSInputFile
import random
import asyncio

# Создаём роутер
router = Router()
user_state = UserState()

@router.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    state = user_state.get_state(user_id)
		
		# Проверка последовательности из 3 сообщений
    last_messages = user_state.get_message_history(user_id)
    if last_messages[-3:] == ["👻", "👻", "👻"]:
        await message.answer("🌀 Тройной квантовый резонанс!")
    
    # Обновляем историю сообщений перед проверкой
    user_state.update_message_history(user_id, message.text)
    
    # Проверка последовательности 👻→👻
    if message.text == "👻" and user_state.get_last_message(user_id) == "👻":
        await message.answer("👾 Активирован режим квантового троллинга!")
        # Сброс истории после активации
        user_state.update_message_history(user_id, "")
        return  # Прерываем дальнейшую обработку
		
    # Логика квантового коллапса
    if random.random() < state.get('collapse_chance', 0.1):
        # Генерация и отправка психоделического графика
        chart_path = generate_pseudoscience_chart(user_id)
        await message.answer_photo(FSInputFile(chart_path))
        await message.answer(f"🌀 Квантовый коллапс! {random_emojis(5)}")
        
        # Сброс параметров
        state.update({
            'collapse_chance': 0.1,
            'banality_level': state.get('banality_level', 0) + 5
        })
        
    else:
        # Генерация обычного ответа
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