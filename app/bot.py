import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from db import init_db, add_subscriber, remove_subscriber, get_subscribers, log_command
from ml_models import classify_image
from utils import get_redis_client

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

redis_client = get_redis_client()
init_db()

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer("Привет! Я бот с интеграцией TensorFlow. Используй /help для списка команд.")

@dp.message(Command("help"))
async def send_help(message: types.Message):
    await message.answer(
        "Доступные команды:\n"
        "/start - Начать\n"
        "/help - Помощь\n"
        "Отправьте фото для классификации."
    )

@dp.message(types.Message.photo)
async def handle_photo(message: types.Message):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    await file.download(destination_file="temp.jpg")

    result = classify_image("temp.jpg")
    await message.answer(f"Результат классификации:\n{result}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
