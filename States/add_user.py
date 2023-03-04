from aiogram.dispatcher.filters.state import State, StatesGroup

class Add_States(StatesGroup):
    type_of_added_user = State()
    user_id = State()