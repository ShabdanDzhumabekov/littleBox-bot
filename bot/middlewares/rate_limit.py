"""
⏱ rate_limit.py — Middleware для ограничения частоты запросов пользователя

Цель:
- Не позволять спамить
- Блокировать повторные нажатия
- Логировать превышение лимитов
"""

import time
import logging
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Union

# Логгер
logger = logging.getLogger(__name__)

class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, limit_seconds: float = 1.0):
        self.limit_seconds = limit_seconds
        # Хранилище времени последнего вызова команды
        self._user_timestamps: Dict[int, float] = {}
        super().__init__()

    async def __call__(self, handler: Callable, event: Union[Message, CallbackQuery], data: Dict[str, Any]):
        user_id = event.from_user.id
        now = time.time()

        last_time = self._user_timestamps.get(user_id, 0)
        if now - last_time < self.limit_seconds:
            logger.info(f"⛔ Rate limit: user {user_id} | type={type(event).__name__}")
            if isinstance(event, Message):
                await event.answer("⏳ Подождите немного перед следующим сообщением.")
            elif isinstance(event, CallbackQuery):
                await event.answer("⏳ Подождите...", show_alert=False)
            return

        self._user_timestamps[user_id] = now
        return await handler(event, data)