from aiogram.dispatcher.filters.state import State, StatesGroup

class Add_States(StatesGroup):
    add_user_type = State()
    add_user_id = State()