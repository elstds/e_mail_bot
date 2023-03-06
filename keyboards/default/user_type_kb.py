from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_type_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Пользователь'),
            KeyboardButton(text='Администратор')
        ]
    ],
    resize_keyboard=True,
)
