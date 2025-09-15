from aiogram import types, Router
from generators.text import generate_thought
from generators.translator import translator
from utils.helpers import random_emojis, dadamizer
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.inline_query()
async def inline_dada(inline_query: types.InlineQuery):
    user_text = inline_query.query.strip()
    result_text = ""
    
    try:
        # Пытаемся обработать введенный текст
        if user_text:
            # Этап 1: Квантовый перевод
            translated = await translator.quantum_translate(user_text, depth=5)
            # Этап 2: Дадаизация
            result_text = dadamizer(translated, chaos_level=5)
        else:
            # Генерируем текст если запрос пустой
            base_text = generate_thought(author=False)
            result_text = dadamizer(base_text, chaos_level=5)
            
    except Exception as e:
        logger.error(f"Dada error: {str(e)}")
        # Фолбек на сгенерированную мысль
        base_text = generate_thought(author=False)
        result_text = dadamizer(base_text, chaos_level=5)

    # Собираем результат
    items = [
        types.InlineQueryResultArticle(
            id="1",
            title="Дадаизируй свой Манифест",
            input_message_content=types.InputTextMessageContent(
                message_text=result_text,
                parse_mode="HTML"
            ),
            description=f"Дадаизируй это → {len(user_text)*'⁑'}" if user_text else "Или просто ЖМИ!"
        )
    ]

    await inline_query.answer(items, cache_time=1)