from aiogram.dispatcher.filters.state import State, StatesGroup


class SearchState(StatesGroup):
    genres = State()
    rating = State()
    search = State()