# Telegram Bot with Mini App

Это Telegram-бот с интеграцией ИИ и мини-приложением для управления функциями.

## Установка

1. Установите Docker и Docker Compose.
2. Создайте файл `.env` с переменными окружения (см. пример ниже).
3. Запустите проект:
   ```bash
   docker-compose up --build
   ```

## Переменные окружения (`.env`)

TELEGRAM_BOT_TOKEN=ваш_токен
DEEPSEEK_API_KEY=ваш_ключ
PUBLICATION_CHANNEL_ID=ваш_канал
DB_NAME=telegram_bot
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379



## Структура проекта

- `app/bot.py` — основной файл бота.
- `app/db.py` — работа с PostgreSQL.
- `app/api.py` — работа с DeepSeek-R1 и Stable Diffusion.
- `app/utils.py` — вспомогательные функции.
- `app/mini_app/` — мини-приложение.

## Команды бота

- `/start` — Начать работу с ботом.
- `/help` — Получить список команд.
- `/generate_text` — Генерация текста.
- `/generate_image` — Генерация изображения.
- `/subscribe` — Подписаться на рассылку.
- `/unsubscribe` — Отписаться от рассылки.
- `/stats` — Получить статистику.

## Лицензия

MIT
# bot
