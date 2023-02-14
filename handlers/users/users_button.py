from aiogram import types
from aiogram.types import CallbackQuery

from data.config import admins_id, users_id
from keyboards.inline.users_kb import users_menu
from loader import dp

@dp.message_handler(text='Пользователи')
async def settings(message: types.Message):
    await message.answer(f'Администраторы:\n{get_users(admins_id)}'
                         f'Пользователи: \n{get_users(users_id)}',
                         reply_markup=users_menu)

def get_users(users):
    result = ''
    for user in users:
        result += f'{user}\n'
    return result
@dp.callback_query_handler(text='add_user')
async def send_message(call: CallbackQuery):
    await call.message.answer("Пользователь добавляется")

@dp.callback_query_handler(text='rm_user')
async def send_message(call: CallbackQuery):
    await call.message.answer("Пользователь удаляется")