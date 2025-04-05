# inline.py
from aiogram import types, Router
from generators.text import generate_thought
from generators.chemical import generate_iupac_name
import random

router = Router()

@router.inline_query()
async def inline_chaos(inline_query: types.InlineQuery):
    items = [
        types.InlineQueryResultArticle(
            id="1",
            title="🔮 Случайная мысль",
            input_message_content=types.InputTextMessageContent(
                message_text=generate_thought()
            ),
            description="Квантовая бессмыслица"
        ),
        types.InlineQueryResultArticle(
            id="2",
            title="🧪 Химический абсурд",
            input_message_content=types.InputTextMessageContent(
                message_text=f"Рекомендуем: {generate_iupac_name()}"
            ),
            description="Сгенерировать формулу"
        )
    ]
    await inline_query.answer(items, cache_time=1)