import random
import aiohttp
from typing import Optional
from generators.translator import translator
from utils.helpers import dadamizer
import logging

logger = logging.getLogger(__name__)

class CASCrafter:
    def __init__(self):
        self.base_api_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cas"
    
    def generate_cas_number(self) -> str:
        """Генерирует валидный CAS-номер с проверочной суммой"""
        def checksum(cas_digits: list) -> int:
            total = sum((i+1)*int(d) for i, d in enumerate(reversed(cas_digits[:-1])))
            return total % 10

        # Генерируем основные части
        part1 = str(random.randint(1000000, 9999999))[-7:]  # 2-7 digits
        part2 = str(random.randint(10, 99))
        
        # Вычисляем контрольную сумму
        digits = list(part1 + part2)
        check_digit = checksum(digits)
        
        return f"{part1}-{part2}-{check_digit}"

    async def get_compound_info(self, cas_number: str) -> Optional[dict]:
        """Получает информацию о веществе через PubChem API"""
        try:
            async with aiohttp.ClientSession() as session:
                # Получаем CID по CAS
                async with session.get(
                    f"{self.base_api_url}/{cas_number}/cids/JSON"
                ) as response:
                    if response.status != 200:
                        return None
                    data = await response.json()
                    cid = data['IdentifierList']['CID'][0]

                # Получаем детальную информацию
                async with session.get(
                    f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/JSON"
                ) as response:
                    if response.status != 200:
                        return None
                    return await response.json()

        except Exception as e:
            logger.error(f"CAS API error: {str(e)}")
            return None

    async def generate_cas_info(self, chaos_level: int = 3) -> str:
        """Генерирует абсурдное описание вещества"""
        cas_number = self.generate_cas_number()
        info = await self.get_compound_info(cas_number)
        
        # Фолбэк если API не ответил
        if not info:
            return dadamizer(
                f"Вещество {cas_number} - квантовая пена в чистом виде! "
                "Все попытки анализа приводят к коллапсу волновой функции.",
                chaos_level
            )

        # Извлекаем данные
        compound_data = info.get('PC_Compounds', [{}])[0]
        name = compound_data.get('id', {}).get('name', 'неизвестно')
        formula = compound_data.get('props', {}).get('MolecularFormula', '???')
        
        # Генерируем описание
        raw_description = (
            f"{name} ({formula}) - "
            "Коллоидный раствор трансцендентальности в матрице бытия. "
            "Способствует квантовой суперпозиции сознания."
        )
        
        # Переводим через цепочку языков
        translated = await translator.quantum_translate(raw_description, depth=3)
        
        # Добавляем дадаистические искажения
        return dadamizer(
            f"🌀 CAS: {cas_number}\n{translated}", 
            chaos_level=chaos_level
        )

# Пример использования
cas_gen = CASCrafter()