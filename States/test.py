from sre_parse import State

from aiogram.dispatcher.filters.state import StatesGroup


class test(StatesGroup):
    test1 = State()
    test2 = State()