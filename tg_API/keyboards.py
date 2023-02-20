from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


advanced_search = InlineKeyboardMarkup()
advanced_search.add(InlineKeyboardButton(text='Жанр', callback_data='Genres'))
advanced_search.add(InlineKeyboardButton(text='Рейтинг', callback_data='Rating'))

genres = InlineKeyboardMarkup()
genres.add(InlineKeyboardButton(text='Экшен', callback_data='Action'))
genres.add(InlineKeyboardButton(text='Комедия', callback_data='Comedy'))
genres.add(InlineKeyboardButton(text='Ужасы', callback_data='Horror'))

top = InlineKeyboardMarkup()
top.add(InlineKeyboardButton(text='Сериалы', callback_data='top_series'))
top.add(InlineKeyboardButton(text='Фильмы', callback_data='top_movies'))

