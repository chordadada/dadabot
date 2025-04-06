import random
import time

class SequenceGenerator:
    def __init__(self):
        self.sequences = {}  # Формат: {user_id: (target, current, timestamp)}
    
    def generate_sequence(self, user_id: int, length: int) -> str:
        seq = ''.join(random.choice('01') for _ in range(length))
        self.sequences[user_id] = (seq, "", time.time())
        return seq
    
    def check_sequence(self, user_id: int, input_bit: str) -> bool:
        data = self.sequences.get(user_id, ("", "", 0.0))
        target, current, timestamp = data
        current += input_bit
        
        # Очистка старых записей (>24 часа)
        if time.time() - timestamp > 86400:
            del self.sequences[user_id]
            return False
        
        self.sequences[user_id] = (target, current, time.time())
        return target.startswith(current)
    
    def calculate_user_progress(self, user_id: int) -> float:
        """Возвращает прогресс пользователя в виде дроби от 0 до 1"""
        data = self.sequences.get(user_id, ("", "", 0.0))
        target, current, _ = data
        return len(current) / len(target) if target else 0.0