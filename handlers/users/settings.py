from aiogram import types
from aiogram.types import CallbackQuery

import data.config
from keyboards.inline.settings_kb import settings_menu
from loader import dp

@dp.message_handler(text='Настройки')
async def settings(message: types.Message):
    await message.answer(f'IMAP сервер: {data.config.imap_server}\n'
                         f'e-mail: {data.config.email_address}\n'
                         f'Рабочие каталоги: {data.config.dirs}',
                         reply_markup=settings_menu)

@dp.callback_query_handler(text='edit_settingss')
async def send_message(call: CallbackQuery):
    await call.message.answer("Настройки редактируются")