import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from db import init_db, add_subscriber, remove_subscriber, get_subscribers, log_command
from api import generate_text, generate_image
from utils import get_redis_client
import asyncio

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Инициализация Redis
redis_client = get_redis_client()

# Инициализация базы данных
init_db()

# Команда /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Привет! Я бот с интеграцией ИИ. Используй /help для списка команд.")

# Команда /help
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.answer(
        "Доступные команды:\n"
        "/start - Начать\n"
        "/help - Помощь\n"
        "/generate_text - Генерация текста\n"
        "/generate_image - Генерация изображения\n"
        "/subscribe - Подписаться на рассылку\n"
        "/unsubscribe - Отписаться от рассылки"
    )

# Команда /generate_text
@dp.message_handler(commands=['generate_text'])
async def handle_generate_text(message: types.Message):
    prompt = message.get_args()
    if not prompt:
        await message.answer("Укажите текст для генерации, например: /generate_text Напиши шутку про кенгуру.")
        return
    ai_text = await generate_text(prompt)
    await message.answer(ai_text)
    log_command(message.from_user.id, 'generate_text')

# Команда /generate_image
@dp.message_handler(commands=['generate_image'])
async def handle_generate_image(message: types.Message):
    prompt = message.get_args()
    if not prompt:
        await message.answer("Укажите запрос для генерации изображения, например: /generate_image кенгуру с ноутбуком.")
        return
    image_url = await generate_image(prompt)
    if image_url:
        await message.answer_photo(image_url)
    else:
        await message.answer("Не удалось сгенерировать изображение.")
    log_command(message.from_user.id, 'generate_image')

# Команда /subscribe
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    add_subscriber(message.from_user.id)
    await message.answer("Вы подписались на рассылку!")
    log_command(message.from_user.id, 'subscribe')

# Команда /unsubscribe
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    remove_subscriber(message.from_user.id)
    await message.answer("Вы отписались от рассылки.")
    log_command(message.from_user.id, 'unsubscribe')

# Рассылка изображений подписчикам
async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        subscribers = get_subscribers()
        for user_id in subscribers:
            image_url = await generate_image("кенгуру с ИИ")
            if image_url:
                await bot.send_photo(user_id, image_url)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(600))  # Рассылка каждые 10 минут
    executor.start_polling(dp, skip_updates=True)
