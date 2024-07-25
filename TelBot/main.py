import asyncio
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

api = '7215043429:AAFU-40Ag6edgj_LZqYv7vVeQesEWVxQeTY'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage)


@dp.message_handler(commands = ['start'])
async def start(message):
    print("Привет! Я бот помогающий твоему здоровью.'")

@dp.message_handler()
async def all_massages(message):
    print("Нужна команда /start.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
