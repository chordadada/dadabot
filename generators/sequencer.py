import logging

logger = logging.getLogger(__name__)

import random
import time

class SequenceGenerator:
    def __init__(self):
        self.sequences = {}  # Формат: {user_id: (target, current, timestamp)}

    def generate_sequence(self, user_id: int, length: int = 5) -> str:
        seq = ''.join(random.choice('01') for _ in range(length))
        self.sequences[user_id] = (seq, "", time.time())
        return seq

    def check_sequence(self, user_id: int, input_bit: str) -> bool:
        if user_id not in self.sequences:
            return False

        target, current, timestamp = self.sequences[user_id]
        new_current = current + input_bit

        # Сброс, если прошло больше 5 минут
        if time.time() - timestamp > 300:
            del self.sequences[user_id]
            return False

        # Проверка прогресса
        if target.startswith(new_current):
            self.sequences[user_id] = (target, new_current, time.time())
            return True
        else:
            del self.sequences[user_id]
            return False

    def is_sequence_complete(self, user_id: int) -> bool:
        if user_id not in self.sequences:
            return False
        target, current, _ = self.sequences[user_id]
        return current == target
				
    def calculate_user_progress(self, user_id: int) -> float:
        if user_id not in self.sequences:
            return 0.0
        target, current, _ = self.sequences[user_id]
        return len(current) / len(target) if len(target) > 0 else 0.0