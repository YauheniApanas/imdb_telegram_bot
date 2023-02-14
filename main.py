from aiogram import executor
import logging
from tg_API.tg_handlers import dp


logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
