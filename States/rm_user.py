from aiogram.dispatcher.filters.state import State, StatesGroup


class RemoveStates(StatesGroup):
    removing_user_id = State()