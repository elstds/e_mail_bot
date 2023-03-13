from aiogram import types
from loader import dp

@dp.message_handler(text='/send_file')
async def command_start(message: types.Message):
    dp.bot.send_file()