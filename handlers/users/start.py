from aiogram import types

from keyboards.default.admin_kb import admin_kb_menu
from loader import dp
from data.config import admins_id, users_id

@dp.message_handler(text='/start')
async def command_start(message: types.Message):
    if message.from_user.id in admins_id:
        await message.answer(f'Привет, {message.from_user.full_name}! \n'
                         'Ты являешься администратором бота', reply_markup=admin_kb_menu)
    elif message.from_user.id in users_id:
        await message.answer(f'Привет, {message.from_user.full_name}! \n'
                         'Ты являешься пользователем бота')
    else:
        await message.answer(f'Привет, {message.from_user.full_name}! \n'
                             f'Твой ID {message.from_user.id}. Сообщи его администратору, чтобы стать пользователем бота.')