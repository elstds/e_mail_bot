from aiogram.dispatcher.filters.state import State, StatesGroup


class SettingStates(StatesGroup):
    choose_setting = State()
    imap_server = State()
    email = State()
    password = State()
    dirs = State()