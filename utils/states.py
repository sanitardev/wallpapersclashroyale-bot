from aiogram.dispatcher.filters.state import State, StatesGroup


class Dialog(StatesGroup):
    add = State()
    delete = State()
