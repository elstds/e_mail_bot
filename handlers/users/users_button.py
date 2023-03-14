from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, KeyboardButton, ReplyKeyboardMarkup

import keyboards.default.admin_kb
from States.add_user import Add_States
from States.rm_user import RemoveStates
from data.config import admins_id, users_id
from keyboards.inline.users_kb import users_menu
from loader import dp
from utils.update_config import update_config
from keyboards.default.user_type_kb import user_type_keyboard
from keyboards.default.cancel import cancel_kb


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
    if call.message.chat.id in admins_id:
        await call.message.answer("Введите тип нового пользователя:", reply_markup=user_type_keyboard)
        await Add_States.add_user_type.set()
    else:
        await call.message.answer(f"Вы не являетесь администратором. Команда не доступна\nID {call.message.chat.id}")


@dp.message_handler(state=Add_States.add_user_type)
async def get_added_user_type(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await message.answer("Добавление пользователя прервано.", reply_markup=keyboards.default.admin_kb.admin_kb_menu)
        await state.finish()
    else:
        user_type = message.text
        await state.update_data(type_of_added_user=user_type)
        await message.answer("Введите ID нового пользователя:", reply_markup=cancel_kb)
        await Add_States.add_user_id.set()


@dp.message_handler(state=Add_States.add_user_id)
async def get_added_user_id(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await message.answer("Добавление пользователя прервано.", reply_markup=keyboards.default.admin_kb.admin_kb_menu)
        await state.finish()
    else:
        global id_
        try:
            id_ = int(message.text)
        except TypeError:
           await message.answer(f"{message.text} не является иденификатором пользователя")
        finally:
            await state.update_data(user_id=id)
            data = await state.get_data()
            user_type = data.get('type_of_added_user')
            await message.answer(f"{user_type} c ID {id_} добавлен")
            if user_type == 'Пользователь':
                users_id.append(id_)
                update_config()
            if user_type == 'Администратор':
                admins_id.append(id_)
            update_config()
        await state.finish()



@dp.callback_query_handler(text='rm_user')
async def send_message(call: CallbackQuery):
    if call.message.chat.id in admins_id:
        await call.message.answer("Введите тип удаляемого пользователя", reply_markup=user_type_keyboard)
        await RemoveStates.removing_user_type.set()
    else:
        await call.message.answer(f"Вы не являетесь администратором. Команда не доступна\nID {call.message.chat.id}")


@dp.message_handler(state=RemoveStates.removing_user_type)
async def get_removing_user_type(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await message.answer("Удаление пользователя прервано.", reply_markup=keyboards.default.admin_kb.admin_kb_menu)
        await state.finish()
    else:
        user_type = message.text
        await state.update_data(type_of_removed_user=user_type)
        await message.answer("Введите ID удаляемого пользователя:", reply_markup=get_removing_users_keyboard(user_type))
        await RemoveStates.removing_user_id.set()

@dp.message_handler(state=RemoveStates.removing_user_id)
async def get_removing_user_id(message: types.Message, state: FSMContext):
    if message.text == "Отмена":
        await message.answer("Удаление пользователя прервано.", reply_markup=keyboards.default.admin_kb.admin_kb_menu)
        await state.finish()
    else:
        global id_
        try:
            id_ = int(message.text)
        except TypeError:
            await message.answer(f"{message.text} не является иденификатором пользователя")
        finally:
            await state.update_data(removed_user_id=id)
            data = await state.get_data()
            user_type = data.get('type_of_removed_user')
            if user_type == 'Пользователь':
                users_id.remove(id_)
                update_config()
            if user_type == 'Администратор':
                admins_id.append(id_)
            update_config()
            await message.answer(f"{user_type} c ID {id_} был удалён", reply_markup=keyboards.default.admin_kb.admin_kb_menu)
    await state.finish()

def get_removing_users_keyboard(type):
    if type == "Пользователь":
        users = users_id
    elif type == "Администратор":
        users = admins_id
    else:
        users = []
    kb = []
    for user in users:
        kb.append([KeyboardButton(text=str(user))])
    kb.append([KeyboardButton(text="Отмена")])
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)