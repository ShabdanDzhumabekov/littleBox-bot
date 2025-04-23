"""
🔐 is_admin.py — Aiogram-фильтр для проверки, является ли пользователь администратором.

Используется для ограничения доступа к командам (например, /feedbacks).
Telegram ID администратора подгружается из переменной окружения.
"""

import os
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from bot.config import ADMIN_ID  # Загружается из .env

class IsAdmin(BaseFilter):
    """
    Кастомный фильтр для проверки, является ли пользователь админом.
    Используется в хендлерах:
        @router.message(IsAdmin())
        @router.callback_query(IsAdmin())
    """
    async def __call__(self, event: Message | CallbackQuery) -> bool:
        return event.from_user.id == ADMIN_ID