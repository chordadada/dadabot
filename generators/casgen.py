import random
import re
import aiohttp
from typing import Optional, Dict
import logging
from pathlib import Path
import json
import asyncio
from utils.helpers import dadamizer

logger = logging.getLogger(__name__)

class CASCrafter:
    def __init__(self, cache_file: str = "cas_cache.json"):
        self.base_api_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cas"
        self.base_dir = Path(__file__).parent
        self.cache_file = self.base_dir / cache_file
        self.cas_database = self._load_cas_database()
        self.cache = self._load_cache()

    def _load_cache(self) -> Dict:
        """Загрузка кеша из файла"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {"compounds": {}}
        except Exception as e:
            logger.error(f"Cache load error: {str(e)}")
            return {"compounds": {}}

    def _load_cas_database(self) -> list:
        """Загрузка и валидация базы CAS-номеров"""
        try:
            db_path = self.base_dir / "cas_database.txt"
            
            # Определение кодировки файла
            with open(db_path, "rb") as f:
                raw_data = f.read()
                detected_encoding = "utf-8"
                try:
                    raw_data.decode("utf-8")
                except UnicodeDecodeError:
                    detected_encoding = "windows-1251"

            # Чтение с правильной кодировкой
            with open(db_path, "r", encoding=detected_encoding) as f:
                lines = [line.strip() for line in f]
                
            valid_cas = []
            invalid_lines = []
            
            for line in lines:
                if self.is_valid_cas(line):
                    valid_cas.append(line)
                else:
                    invalid_lines.append(line)
            
            logger.info(f"Loaded {len(valid_cas)} valid CAS numbers")
            if invalid_lines:
                logger.warning(f"Found {len(invalid_lines)} invalid entries. Examples: {invalid_lines[:3]}")
            
            if not valid_cas:
                raise ValueError("No valid CAS numbers in database")
            
            return valid_cas
            
        except Exception as e:
            logger.critical(f"Database error: {str(e)}")
            return []

    @staticmethod
    def is_valid_cas(cas_number: str) -> bool:
        """Проверка валидности CAS-номера"""
        if not re.fullmatch(r'\d{2,7}-\d{2}-\d', cas_number):
            return False
        parts = cas_number.split("-")
        digits = parts[0] + parts[1] + parts[2]
        try:
            check_digit = int(digits[-1])
            total = sum((i+1) * int(d) for i, d in enumerate(reversed(digits[:-1])))
            return total % 10 == check_digit
        except:
            return False

    def generate_cas_number(self) -> str:
        """Генерация из локальной базы"""
        if not self.cas_database:
            raise ValueError("CAS database is empty or invalid")
        return random.choice(self.cas_database)

    async def get_compound_info(self, cas_number: str) -> Optional[dict]:
        """Получение информации о соединении"""
        if cached := self.cache["compounds"].get(cas_number):
            logger.debug(f"Using cached data for {cas_number}")
            return cached
        
        try:
            async with aiohttp.ClientSession() as session:
                # Получение CID
                async with session.get(
                    f"{self.base_api_url}/{cas_number}/cids/JSON",
                    timeout=10
                ) as response:
                    if response.status != 200:
                        return None
                    data = await response.json()
                    cid = data['IdentifierList']['CID'][0]

                # Получение деталей
                async with session.get(
                    f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/JSON",
                    timeout=10
                ) as response:
                    if response.status != 200:
                        return None
                    result = await response.json()
                    self.cache["compounds"][cas_number] = result
                    self._save_cache()
                    return result

        except Exception as e:
            logger.error(f"API error: {str(e)}")
            return None

    def _save_cache(self):
        """Сохранение кеша"""
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            logger.error(f"Cache save error: {str(e)}")

    async def generate_cas_info(self, chaos_level: int = 3) -> str:
        """Генерация психоделического описания"""
        try:
            cas_number = self.generate_cas_number()
            info = await self.get_compound_info(cas_number)
            
            # Извлечение реальных данных
            name = "Квантовая пена"
            formula = "∅"
            props = []
            if info:
                compound = info.get('PC_Compounds', [{}])[0]
                name = compound.get('id', {}).get('name', 'Хаос-конденсат')
                formula = compound.get('props', {}).get('MolecularFormula', '⚡⃤')
                
                # Сбор случайных свойств
                for prop in compound.get('props', []):
                    if 'value' in prop:
                        props.append(f"{prop.get('label', 'Свойство')}: {prop['value']}")

            # Дадаистические трансформации
            elements = [
                f"🌀 *{cas_number}*", 
                f"**{name.upper()}** ({formula})",
                random.choice([
                    "Синтез 11-мерных вихрей",
                    "Экстракт платоновых тел",
                    "Сублимация энтропийных волн"
                ]),
                "Эффекты:",
                "▸ Квантовая суперпозиция сознания",
                "▸ Трансгрессия хиральных границ",
                "▸ Обратная диффузия времени" + random.choice(["²³⁵U", "🔄", "⊛"]),
                random.choice([">! НЕ ДЛЯ ТЕРРАН !<", "⚠️ НЕ СМЕШИВАТЬ С РЕАЛЬНОСТЬЮ"]),
                "Побочные действия:",
                "✓ Спонтанная телепортация", 
                "✓ Полиморфизм идентичности",
                "✓ Когнитивный градиентный взрыв"
            ]

            # Добавляем реальные свойства если есть
            if props:
                elements.insert(3, f"Параметры:\n▸ " + "\n▸ ".join(random.sample(props, min(3, len(props)))))
            
            # Собираем всё в текстовый коллаж
            base_text = "\n".join(elements)
            
            # Финальная обработка
            return dadamizer(
                text=base_text,
                chaos_level=chaos_level
            )
            
        except Exception as e:
            logger.error(f"Квантовый коллапс: {str(e)}")
            return dadamizer("♻️ Реальность перезагружается... Попробуйте позже", chaos_level)

cas_gen = CASCrafter()