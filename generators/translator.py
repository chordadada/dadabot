import random
import aiohttp
from typing import Optional
from config.settings import config
import logging

logger = logging.getLogger(__name__)

class QuantumTranslator:
    def __init__(self):
        #self.transit_langs = ['it', 'hu', 'fi', 'nl', 'el', 'ga', 'mt', 'pl', 'sk', 'tr', 'uk', 'sq', 'de', 'fr', 'es', 'pt', 'ro']
        self.transit_langs = ['zh', 'ja', 'ar', 'fi', 'hu', 'tr', 'th', 'vi', 'ko', 'bn', 'tl', 'sw', 'fa', 'he', 'ur', 'id']
        self.final_lang = 'ru'
        self.max_depth = 5
        self.api_url = "https://api.mymemory.translated.net/get"

    async def _translate_segment(
        self,
        text: str,
        source_lang: str,
        target_lang: str
    ) -> Optional[str]:
        try:
            if source_lang == target_lang:
                logger.warning(f"Попытка перевода {source_lang}→{target_lang} (одинаковые языки)")
                return None

            params = {
                'q': text,
                'langpair': f'{source_lang}|{target_lang}',
                'key': getattr(config, 'TRANSLATION_KEY', '')
            }
            
            logger.debug(f"Запрос перевода: {source_lang}→{target_lang}")
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.api_url,
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=15)
                ) as response:
                    data = await response.json()
                    if response.status != 200:
                        logger.error(f"Ошибка API: {data.get('responseStatus', 'Unknown')}")
                        return None
                    return data['responseData']['translatedText']
        
        except Exception as e:
            logger.error(f"Ошибка перевода {source_lang}→{target_lang}: {str(e)}")
            return None

    async def quantum_translate(
        self,
        text: str,
        depth: int
    ) -> str:
        current_text = text
        lang_chain = []
        detected_lang = self.detect_language(text)
        last_lang = detected_lang
        used_langs = set()

        logger.info(f"Начало перевода. Исходный язык: {detected_lang}, глубина: {depth}")

        try:
            for step in range(depth):
                available_langs = [
                    lang for lang in self.transit_langs
                    if lang != last_lang
                    and lang != self.final_lang
                    and lang not in used_langs
                ]
                
                if not available_langs:
                    available_langs = [
                        lang for lang in self.transit_langs
                        if lang != last_lang
                        and lang != self.final_lang
                    ]
                    used_langs.clear()

                if not available_langs:
                    break

                next_lang = random.choice(available_langs)
                used_langs.add(next_lang)

                translated = await self._translate_segment(current_text, last_lang, next_lang)
                if not translated:
                    break
                
                #lang_chain.append(f"{last_lang}→{next_lang}")
                current_text = translated
                last_lang = next_lang

            # Финальный перевод без добавления в цепочку
            if last_lang != self.final_lang:
                final_translation = await self._translate_segment(current_text, last_lang, self.final_lang)
                if final_translation:
                    current_text = final_translation

            # return f"{current_text}\n\n🌀 Цепочка: {' → '.join(lang_chain)}"
            return f"{current_text}"

        except Exception as e:
            logger.error(f"Критическая ошибка: {str(e)}")
            return "🌀 Квантовый коллапс! Попробуйте позже."

    def detect_language(self, text: str) -> str:
        cyrillic_chars = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        return 'ru' if any(c in cyrillic_chars for c in text.lower()) else 'en'

translator = QuantumTranslator()