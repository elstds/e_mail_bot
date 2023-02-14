from aiogram import types

from keyboards.default.admin_kb import admin_kb_menu
from loader import dp
from data.config import admins_id, users_id

@dp.message_handler(text='Цикл')
async def command_start(message: types.Message):
    while True:
        await dp.bot.send_message(chat_id=message.from_user.id, text='Цикл')