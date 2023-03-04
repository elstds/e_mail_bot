from aiogram import types, Dispatcher

async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Запустить бота'),
        types.BotCommand('help', 'Помощь'),
        types.BotCommand('start_mailing', 'Запустить рассылку'),
        types.BotCommand('stop_mailing', 'Остановить рассылку')
    ])