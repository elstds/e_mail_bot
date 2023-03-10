from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from States import CommonStates
from data.config import admins_id
from loader import dp


@dp.message_handler(Command("help"))
async def help(message: types.message):
    text = '''
    Команда /start выводит ваш статус пользователя и идентификатор, если вы не зарегистрированы.
    Простым пользователям доступны только команды /start и /help, они могут лишь получать сообщения. Администраторы могут выполнять команды и редактировать конфигурации.
    Команда /start_mailing запускает рассылку, если запущена в стандартном режиме, иногда запускается со второго раза, бот сообщит, когда рассылка начнется.
    Команда /stop_mailing останавливает рассылку, если она запущена.
    '''
    await message.answer(text)