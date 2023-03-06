from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_kb_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Настройки'),
            KeyboardButton(text='Пользователи')
        ]
    ],
    resize_keyboard=True,
)
