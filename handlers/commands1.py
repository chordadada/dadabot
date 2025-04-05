from aiogram import types, F
from aiogram.fsm.context import FSMContext
from states.user_states import UserState
import random

user_state = UserState()

async def cmd_start(message: types.Message, state: FSMContext):
    keyboard = [
        [types.KeyboardButton(text="ДА"), types.KeyboardButton(text="НЕТ")],
        [types.KeyboardButton(text="👻"), types.KeyboardButton(text="Взрыв")],
        [types.KeyboardButton(text="Искусство"), types.KeyboardButton(text="Кот Шрёдингера")]
    ]
    markup = types.ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    await message.answer("Вы согласны с тем, что ничего не согласны?", reply_markup=markup)
    print(f"🌀 Пользователь {message.from_user.id} начал квантовый диалог")