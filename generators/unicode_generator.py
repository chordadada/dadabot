from typing import List
from functools import lru_cache
import random

def generate_text_variants(base_text: str) -> List[str]:
    """Генерирует варианты символов с разными Unicode-представлениями"""
    variants = []
    
    # Маппинг для каждого символа базового текста
    char_map = {
        'D': ['D', '𝐃', '𝐷', '𝑫', '𝔻', '𝕯', 'Ｄ', '🅳', '🄳'],
        'a': ['a', '𝑎', '𝒂', '𝖆', '𝕒', 'ａ', '🅰', '🄰', 'ä', 'å'],
        'Д': ['Д', 'Д', 'ᗪ', 'ᗞ', 'ꓒ', 'ꝉ'],
        'д': ['д', 'д', '∂', 'ꝋ', 'Ꝋ']
    }
    
    # Генерация всех комбинаций
    for first in char_map.get(base_text[0], [base_text[0]]):
        for second in char_map.get(base_text[1], [base_text[1]]):
            variants.append(f"{first}{second}")
    
    return variants

@lru_cache(maxsize=10)
def get_cached_variants(base: str = "Da") -> List[str]:
    """Кешированные варианты с фильтрацией"""
    variants = generate_text_variants(base) + generate_text_variants("Да")
    return filter_supported_variants(variants)

def filter_supported_variants(variants: List[str]) -> List[str]:
    """Фильтрация неподдерживаемых символов"""
    supported = []
    for variant in variants:
        try:
            variant.encode('utf-8').decode('utf-8')
            supported.append(variant)
        except UnicodeError:
            continue
    return list(set(supported))  # Удаление дубликатов