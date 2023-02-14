from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

settings_menu = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Изменить...", callback_data='edit_settingss')
        ]
    ]
)