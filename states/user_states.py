import time
import random


class UserState:
    def __init__(self):
        self.users = {}
        self.message_history = {}
        self.entangled_pairs = []
        self.achievements = {
        'quantum_rebel': False,
        'paradox_master': False
        }
        self.ghost_emoji = "👻"
        self.ghost_data = {
            "current_emoji": "👻",
            "visibility": True
        }

    def get_state(self, user_id: int) -> dict:
        if user_id not in self.users:
            self.users[user_id] = {
                'banality_level': 0,
                'quantum_entangled_with': None,
                'last_interaction': time.time(),
								'quantum_events': 0,
                'collapse_chance': 0.1
            }
        return self.users[user_id]

    def entangle_users(self, user1: int, user2: int):
        self.users[user1]['quantum_entangled_with'] = user2
        self.users[user2]['quantum_entangled_with'] = user1
        self.entangled_pairs.append((user1, user2))

    def get_last_message(self, user_id: int) -> str:
        """Возвращает последнее сообщение пользователя"""
        return self.message_history.get(user_id, "")

    def update_message_history(self, user_id: int, message: str, max_history=5):
        """Хранит только последние 5 сообщений"""
        if user_id not in self.message_history:
          self.message_history[user_id] = []
        self.message_history[user_id].append(message)
        self.message_history[user_id] = self.message_history[user_id][-max_history:]
			
    def get_message_history(self, user_id: int) -> list:
        """Возвращает все сохраненные сообщения"""
        return self.message_history.get(user_id, [])

    def reset_states(self):
        for user in self.users:
            self.users[user]['banality_level'] = 0

    def check_achievements(self, user_id):
        if self.users[user_id]['collapse_count'] >= 10 and not self.achievements['quantum_rebel']:
            self.achievements['quantum_rebel'] = True
            return "🔮 Вы стали Квантовым хулиганом!"
				
    def update_ghost_state(self):
        """Обновляет состояние кнопки-призрака"""
        self.ghost_data["current_emoji"] = random.choice(["👻", "👀", "💨", "🌀"])
        self.ghost_data["visibility"] = random.random() > 0.2
        return self.ghost_data
				
    def update_ghost_emoji(self):
        from utils.helpers import random_emojis
        self.ghost_emoji = random_emojis(1, emoji_set=random.choice(["magic", "science"]))
        return self.ghost_emoji