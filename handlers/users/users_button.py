from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from States.add_user import Add_States
from States.rm_user import RemoveStates
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
    await call.message.answer("Введите тип нового пользователя:")
    await Add_States.type_of_added_user.set()


@dp.message_handler(state=Add_States.type_of_added_user)
async def get_user_type(message: types.Message, state: FSMContext):
    user_type = message.text
    await state.update_data(type_of_added_user=user_type)
    await message.answer("Введите ID нового пользователя:")
    await Add_States.user_id.set()


@dp.message_handler(state=Add_States.user_id)
async def get_user_id(message: types.Message, state: FSMContext):
    id_ = message.text
    await state.update_data(user_id=id)
    data = await state.get_data()
    user_type = data.get('type_of_added_user')
    await message.answer(f"{user_type} c ID {id_} добавлен")
    await state.finish()



@dp.callback_query_handler(text='rm_user')
async def send_message(call: CallbackQuery):
    await call.message.answer("Введите ID удаляемого пользователя")
    await RemoveStates.removing_user_id.set()


@dp.message_handler(state=RemoveStates.removing_user_id)
async def get_removing_user_id(message: types.Message, state: FSMContext):
    id_ = message.text
    await state.update_data(removing_user_id=id_)
    await message.answer(f"Польлзователь с id {id_} удаляется")
    await state.finish()
