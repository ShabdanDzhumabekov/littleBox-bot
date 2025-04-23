"""
📊 stats.py — Хендлер для отображения статистики бота

Функции:
- Команда /stats (доступна только администратору)
- Показывает общее количество пользователей, объявлений, маршрутов, отзывов
"""

from aiogram import Router, types, F
from aiogram.filters import Command
from sqlalchemy import select, func

from bot.database.db import get_session
from bot.database.models import User, Ad, Route, Feedback
from bot.filters.is_admin import IsAdmin

router = Router()

@router.message(Command("stats"), IsAdmin())
@router.message(F.text == "📊 Статистика", IsAdmin())
async def show_stats(message: types.Message):
    """
    Показывает общую статистику по базе данных (только для админа).
    """
    async for session in get_session():
        users_count = await session.scalar(select(func.count()).select_from(User))
        ads_count = await session.scalar(select(func.count()).select_from(Ad))
        routes_count = await session.scalar(select(func.count()).select_from(Route))
        feedbacks_count = await session.scalar(select(func.count()).select_from(Feedback))

        text = (
            "📊 <b>Статистика LittleBox:</b>\n"
            f"👥 Пользователей: <b>{users_count}</b>\n"
            f"📦 Объявлений: <b>{ads_count}</b>\n"
            f"🛫 Маршрутов: <b>{routes_count}</b>\n"
            f"💬 Отзывов: <b>{feedbacks_count}</b>"
        )
        await message.answer(text, parse_mode="HTML")