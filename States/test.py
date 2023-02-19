from aiogram.dispatcher.filters.state import State, StatesGroup


class BotStates(StatesGroup):
    getting = State()
    mailing = State()
