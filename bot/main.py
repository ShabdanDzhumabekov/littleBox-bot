"""
Главный файл запуска Telegram-бота 📦

Функции:
- Инициализация бота с токеном
- Установка формата сообщений (HTML)
- Настройка памяти для FSM (машины состояний)
- Подключение маршрутов (handlers)
- Запуск бота через polling

Совместимо с aiogram 3.7+
"""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from bot.config import BOT_TOKEN                    # Загрузка токена из .env  
from bot.handlers import setup_routers              # Хендлеры, например: /start

# Настраиваем логгирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

async def main():
    """
    Главная асинхронная функция для запуска бота
    """

    # Инициализация бота с HTML-разметкой по умолчанию
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    # Создаём диспетчер с хранением состояний в оперативной памяти
    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем все зарегистрированные обработчики (например, /start)
    dp.include_router(setup_routers())

    # Запускаем бота
    logging.info("🤖 Bot is starting...")
    await dp.start_polling(bot)

# Точка входа
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("⛔ Bot stopped.")