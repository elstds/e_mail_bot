from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

users_menu = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Добавить пользоавтеля", callback_data='add_user'),
            InlineKeyboardButton(text="Удалить пользоавтеля", callback_data='rm_user')
        ]
    ]
)