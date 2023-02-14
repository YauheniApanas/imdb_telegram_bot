from aiogram import Bot, Dispatcher, types
from config import config

bot = Bot(token=config.tg_token.get_secret_value())
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def say_hello(message: types.Message):
    await message.answer(text='Hello')

