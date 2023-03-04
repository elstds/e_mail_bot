from aiogram.dispatcher.filters.state import State, StatesGroup


class CommonStates(StatesGroup):
    base = State()
    mailing = State()

