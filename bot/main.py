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
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from bot.config import BOT_TOKEN                            # Загрузка токена из .env
from bot.handlers import start, help, ads, routes           # Хендлеры, например: /start

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
    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(ads.router)
    dp.include_router(routes.router)

    # Запускаем бота
    await dp.start_polling(bot)

# Точка входа
if __name__ == "__main__":
    asyncio.run(main())