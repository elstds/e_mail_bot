from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from imaplib import IMAP4_SSL

import data.config
from keyboards.inline.settings_kb import settings_menu
from keyboards.default.settings_kb import settings_choose
from keyboards.default.admin_kb import admin_kb_menu
from keyboards.default.cancel import cancel_kb
from States.settings import SettingStates
from loader import dp
from utils.update_config import update_config




@dp.message_handler(text='Настройки')
async def settings(message: types.Message):
    if message.from_user.id in data.config.admins_id:
        list = "\n".join(dirs())
        await message.answer(f'IMAP сервер: {data.config.imap_server}\n'
                             f'e-mail: {data.config.email_address}\n'
                             f'Рабочие каталоги: {list}',
                             reply_markup=settings_menu)
    else:
        await message.answer("Вы не являетесть администратором.")


def dirs():
    imap = IMAP4_SSL(data.config.imap_server)
    sts, res = imap.login(data.config.email_address, data.config.password)
    if sts == 'Ok':
        sts, boxes = imap.list()
        if sts == 'Ok':
            true_boxes = []
            for box in boxes:
                true_boxes.append(box[2:-1])
            return true_boxes
        else:
            imap.logout()
            return ['Error']
    else:
        imap.logout()
        return ['Error']



@dp.callback_query_handler(text='edit_settingss')
async def send_message(call: CallbackQuery):
    if call.message.chat.id in data.config.admins_id:
        await call.message.answer("Изменить параметр: ", reply_markup=settings_choose)
        await SettingStates.choose_setting.set()
    else:
        await call.message.answer("Вы не являетесь администратором")


@dp.message_handler(state=SettingStates.choose_setting)
async def choose(message: types.Message, state: FSMContext):
    if message.text == "IMAP сервер":
        await message.answer("Введите новый адрес imap сервера:", reply_markup=cancel_kb)
        await SettingStates.imap_server.set()
    elif message.text == "Учетная запись":
        await message.answer("Введите новый адрес электронной почты:", reply_markup=cancel_kb)
        await SettingStates.email.set()
    elif message.text == "Рабочие каталоги":
        await message.answer("Введите названия каталогов через пробел:")
        await SettingStates.dirs.set()
    elif message.text == "Отмена":
        await message.answer(text="Редактирование параметров отменено", reply_markup=admin_kb_menu)
        await state.finish()
    else:
        await message.answer("Вы выбрали неверный параметр")


@dp.message_handler(state=SettingStates.imap_server)
async def set_imap_server(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer("Редактирование конфигурации отменено.", reply_markup=admin_kb_menu)
        await state.finish()
    else:
        new_imap = message.text
        data.config.imap_server = new_imap
        update_config()
        await message.answer("IMAP сервер обновлён.", reply_markup=admin_kb_menu)
        await state.finish()


@dp.message_handler(state=SettingStates.email)
async def set_email(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer("Редактирование конфигурации отменено.", reply_markup=admin_kb_menu)
        await state.finish()
    else:
        new_email = message.text
        await state.update_data(new_email=new_email)
        await message.answer("Введите пароль:", reply_markup=cancel_kb)
        await SettingStates.password.set()


@dp.message_handler(state=SettingStates.password)
async def set_password(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer("Редактирование конфигурации отменено.", reply_markup=admin_kb_menu)
        await state.finish()
    else:
        storage = await state.get_data()
        data.config.email_address = storage.get("new_email")
        data.config.password = message.text
        update_config()
        await message.answer("Параметры учетной запись обновлены.", reply_markup=admin_kb_menu)
        await state.finish()


@dp.message_handler(state=SettingStates.dirs)
async def set_dirs(message: types.Message, state: FSMContext):
    if message.text == 'q':
        await message.answer("Редактирование конфигурации отменено.")
        await state.finish()
    else:
        data.config.dirs = message.text.split()
        update_config()
        await message.answer("Каталоги обновлены.")
        await state.finish()
