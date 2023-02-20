from aiogram import Bot, Dispatcher, types
from config import config
from typing import List
from site_API.site_handlers import search as api_search, get_info, genres_search, rating_search as api_rating_search,\
    get_series, get_movies
import tg_API.keyboards as keyboards
from database.CRUD import save as db_save, retrieve_collection as db_retrieve_collection

bot = Bot(token=config.tg_token.get_secret_value())
dp = Dispatcher(bot)
movies = list()
current = 0


@dp.message_handler(commands=['start'])
async def say_hello(message: types.Message):
    await message.answer(text='Hello')


@dp.message_handler(commands=['help'])
async def help_message(message: types.message):
    await bot.send_message(message.from_user.id, text='search — поиск по названию\n'
                                                      'favourite — ваша коллекция фильмов\n'
                                                      'advanced — расширенный поиск по жанру/рейтингу\n'
                                                      'top — топ 250 фильмов/сериалов.')


@dp.message_handler(commands=['search'])
async def enter_search(message: types.message):
    await bot.send_message(message.from_user.id, text='Введите название:')

    @dp.message_handler(content_types=['text'])
    async def search(title: types.message):
        result = api_search(title=str(title['text']))
        builder = types.InlineKeyboardMarkup()
        for i_title in result.keys():
            builder.add(types.InlineKeyboardButton(text=i_title, callback_data=result[i_title]))
        await bot.send_message(message.from_user.id, reply_markup=builder,
                               text='Результаты поиска, выберите подходящий:')


@dp.message_handler(commands=['favourite'])
async def get_favourite(message: types.Message):
    global movies
    global current
    current = 0
    user_collection = db_retrieve_collection(message.from_user.id)
    if user_collection:
        movies = user_collection
        await print_results(callback=message)
    else:
        await bot.send_message(message.from_user.id, text='Вы еще не добавили ничего в свою коллекцию')


@dp.callback_query_handler(lambda ttl: ttl.data and ttl.data.startswith('tt'))
async def get_full_info(callback: types.CallbackQuery):
    info = get_info(callback.data)
    title_id = info['id']
    builder = types.InlineKeyboardMarkup()
    builder.add(types.InlineKeyboardButton(text='Трейлер', url=info['trailer']))
    builder.add(types.InlineKeyboardButton(text='Сохранить', callback_data=f'Save {title_id}'))
    if len(info['similars']) > 3:
        for i_similar in range(3):
            similar_title = info['similars'][i_similar]['title']
            similar_id = info['similars'][i_similar]['id']
            builder.add(types.InlineKeyboardButton(text=f'Похожее: {similar_title}', callback_data=similar_id))
    else:
        for i_similar in range(len(info['similars'])):
            similar_title = info['similars'][i_similar]['title']
            similar_id = info['similars'][i_similar]['id']
            builder.add(types.InlineKeyboardButton(text=f'Похожее: {similar_title}', callback_data=similar_id))

    info_string = f"<b>{info['title']}</b>" \
                  f"\n<b>{info['genre']}</b>" \
                  f"\n<b>Сюжет</b>: {info['plot']}" \
                  f"\n<b>Режиссёр:</b> {info['directors']}" \
                  f"\n<b>Страны:</b> {info['countries']}" \
                  f"\n<b>Рейтинг:</b> {info['rating']}" \
                  f"\n<b>Дата выпуска в прокат:</b> {info['date']}"
    if info['image'].endswith('jpg'):
        await bot.send_photo(callback.from_user.id, info['image'])
    await bot.send_message(callback.from_user.id, reply_markup=builder, text=info_string, parse_mode='HTML')


@dp.callback_query_handler(lambda text: text.data and text.data.startswith('Save'))
async def saving(callback: types.CallbackQuery):
    tt = callback.data.split()[1]
    title = callback.message['text'].split('\n')[0]
    await save(user=callback.from_user.id, title_id=tt, title=title)


async def save(title_id: str, title: str, user):
    db_save(user=user, title_id=title_id, title=title)
    print(title)


@dp.message_handler(commands=['advanced'])
async def choose_category(message: types.message):
    await bot.send_message(message.from_user.id, text='Выбор категории поиска: ',
                           reply_markup=keyboards.advanced_search)


@dp.callback_query_handler(text='Genres')
async def genre_search(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, text='Выбор жанра', reply_markup=keyboards.genres)


@dp.callback_query_handler(text='Rating')
async def rating_search(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, text='Минимальный рейтинг и максимальный рейтинг(через пробел):')

    @dp.message_handler(content_types=['text'])
    async def get_rating(message: types.Message):
        global movies
        movies = api_rating_search(message['text'])
        await print_results(callback=callback)


@dp.message_handler(commands=['top'])
async def which_top(message: types.message):
    await bot.send_message(message.from_user.id, reply_markup=keyboards.top, text='Выбор:')


@dp.callback_query_handler(text='top_series')
async def get_top_series(callback: types.CallbackQuery):
    global movies
    global current
    current = 0
    movies = get_series()
    await print_results(callback=callback)


@dp.callback_query_handler(text='top_movies')
async def get_top_movies(callback: types.CallbackQuery):
    global movies
    global current
    current = 0
    movies = get_movies()
    await print_results(callback=callback)


@dp.callback_query_handler(text='Action')
async def action_search(callback: types.CallbackQuery):
    global movies
    global current
    current = 0
    movies = genres_search('action')
    await print_results(callback=callback)


@dp.callback_query_handler(text='Comedy')
async def comedy_search(callback: types.CallbackQuery):
    global movies
    global current
    current = 0
    movies = genres_search('comedy')
    await print_results(callback=callback)


@dp.callback_query_handler(text='Horror')
async def horror_search(callback: types.CallbackQuery):
    global movies
    global current
    current = 0
    movies = genres_search('horror')
    await print_results(callback=callback)


async def print_results(callback):
    global movies
    global current
    print('printresult:', current, movies)
    keyboard = types.InlineKeyboardMarkup()
    if len(movies) > 5:
        for i_title in range(0, 5):
            keyboard.add(types.InlineKeyboardButton(text=movies[i_title]['title'], callback_data=movies[i_title]['id']))
        keyboard.add(types.InlineKeyboardButton(text='Больше', callback_data=f'more'))
        await bot.send_message(callback.from_user.id, text='Результаты поиска: ', reply_markup=keyboard)
    elif len(movies) <= 5:
        for i_title in range(0, len(movies)):
            keyboard.add(types.InlineKeyboardButton(text=movies[i_title]['title'], callback_data=movies[i_title]['id']))
        await bot.send_message(callback.from_user.id, text='Результаты поиска: ', reply_markup=keyboard)

    @dp.callback_query_handler(text='more')
    async def more_movies(callback_more: types.CallbackQuery = callback):
        global current
        global movies
        current += 5
        movies = movies[5:]
        print('after more: ', current, movies)
        await print_results(callback=callback_more)

