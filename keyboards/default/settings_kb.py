from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

settings_choose = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='IMAP сервер'),
            KeyboardButton(text='Учетная запись'),
            KeyboardButton(text="Рабочие каталоги")
        ],
        [
            KeyboardButton(text="Отмена")
        ]
    ],
    resize_keyboard=True,
)
