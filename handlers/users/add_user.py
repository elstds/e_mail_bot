from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp

@dp.message_handler(Command('/add_user'))
async def adduser(message: types.Message):
    await message.answer()