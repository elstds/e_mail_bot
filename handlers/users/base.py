from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from States import CommonStates
from data.config import admins_id
from loader import dp


@dp.message_handler(Command("stop_mailing"))
async def stop_mailing(message: types.Message):
    if message.from_user.id in admins_id:
        # await CommonStates.base.set()
        pass
    else:
        await message.answer("Вы не являетесь администратором")


@dp.message_handler(state=CommonStates.base)zlib
async def base(message: types.Message, state: FSMContext):
    if message.from_user.id:
        await message.answer("Рассылка отключена")
