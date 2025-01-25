import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from db import init_db, add_subscriber, remove_subscriber, get_subscribers, log_command
from ml_models import classify_image
from utils import get_redis_client
import asyncio

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

redis_client = get_redis_client()
init_db()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Привет! Я бот с интеграцией TensorFlow. Используй /help для списка команд.")

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.answer(
        "Доступные команды:\n"
        "/start - Начать\n"
        "/help - Помощь\n"
        "Отправьте фото для классификации."
    )

@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await file.download(destination_file="temp.jpg")

    result = classify_image("temp.jpg")
    await message.answer(f"Результат классификации:\n{result}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
