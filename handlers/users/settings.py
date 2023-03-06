from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

import data.config
from keyboards.inline.settings_kb import settings_menu
from keyboards.default.settings_kb import settings_choose
from keyboards.default.admin_kb import admin_kb_menu
from States.settings import SettingStates
from loader import dp

@dp.message_handler(text='Настройки')
async def settings(message: types.Message):
    if message.from_user.id in data.config.admins_id:
        await message.answer(f'IMAP сервер: {data.config.imap_server}\n'
                         f'e-mail: {data.config.email_address}\n'
                         f'Рабочие каталоги: {data.config.dirs}',
                         reply_markup=settings_menu)
    else:
        await message.answer("Вы не являетесть администратором.")

@dp.callback_query_handler(text='edit_settingss')
async def send_message(call: CallbackQuery):
    await call.message.answer("Изменить параметр: ", reply_markup=settings_choose)
    await SettingStates.choose_setting.set()


@dp.message_handler(state=SettingStates.choose_setting)
async def choose(message: types.Message, state: FSMContext):
    if message.text == "IMAP сервер":
        await SettingStates.imap_server.set()
    elif message.text == "Учетная запись":
        await SettingStates.email.set()
    elif message.text == "Рабочие каталоги":
        await SettingStates.dirs.set()
    elif message.text == "Отмена":
        await message.answer(text="Редактирование параметров отменено",  reply_markup=admin_kb_menu)
        await state.finish()
    else:
        await message.answer("Вы выбрали неверный параметр")

@dp.message_handler(state=SettingStates.imap_server)
async def set_imap_server(message: types.Message, state: FSMContext):
    await state.finish()

@dp.message_handler(state=SettingStates.email)
async def set_email(message:types.Message, state: FSMContext):
    await state.finish()

@dp.message_handler(state=SettingStates.dirs)
async def set_dirs(message: types.Message, state: FSMContext):
    await state.finish()