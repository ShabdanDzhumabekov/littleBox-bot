"""
🔔 notifications.py — Уведомления пользователей о совпадениях

Функции:
- При добавлении маршрута проверяет совпадения с объявлениями
- При добавлении объявления проверяет совпадения с маршрутами
- Отправляет уведомления соответствующим пользователям

Механизм:
- Использует SQLAlchemy для поиска совпадений по полям: from_city, from_country, to_city, to_country
- Исключает отправку уведомления самому себе
- Форматирует сообщение через функции format_ad и format_route
"""

import logging
from datetime import date

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from bot.database.models import Ad, Route, User
from bot.database.db import SessionLocal
from bot.utils import format_ad, format_route, format_author

logger = logging.getLogger(__name__)


async def notify_about_new_ad(bot: Bot, ad_id: int):
    """
    Уведомляет пользователей, у которых есть подходящие маршруты под новое объявление.

    :param bot: Экземпляр Telegram-бота
    :param ad: Объект объявления (Ad), только что добавленного
    """
    async with SessionLocal() as session:
        ad = await session.get(Ad, ad_id, options=[selectinload(Ad.user)])  # сразу загрузи user
        if not ad:
            return

        stmt = select(Route, User).join(User).where(
            Route.from_city == ad.from_city,
            Route.from_country == ad.from_country,
            Route.to_city == ad.to_city,
            Route.to_country == ad.to_country,
            Route.travel_date >= date.today()
        )
        result = await session.execute(stmt)
        matches = result.all()

        for route, user in matches:
            # Не уведомляем автора
            if user.telegram_id != ad.user.telegram_id:
                await _send_notification(
                    bot,
                    user.telegram_id,
                    "📦 Появилось новое объявление, подходящее под ваш маршрут:\n\n" +
                    format_ad(ad) + "\n" +
                    format_author(ad.user)
                )


async def notify_about_new_route(bot: Bot, route_id: int):
    """
    Уведомляет пользователей, у которых есть подходящие объявления под новый маршрут.

    :param bot: Экземпляр Telegram-бота
    :param route: Объект маршрута (Route), только что добавленного
    """
    async with SessionLocal() as session:
        route = await session.get(Route, route_id, options=[selectinload(Route.user)])
        if not route:
            return 

        stmt = select(Ad, User).join(User).where(
            Ad.from_city == route.from_city,
            Ad.from_country == route.from_country,
            Ad.to_city == route.to_city,
            Ad.to_country == route.to_country,
            Ad.approx_date >= date.today()
        )
        result = await session.execute(stmt)
        matches = result.all()

        for ad, user in matches:
            # Не уведомляем автора
            if user.telegram_id != route.user.telegram_id:
                await _send_notification(
                    bot,
                    user.telegram_id,
                    "🛫 Появился путешественник, подходящий под ваше объявление:\n\n" +
                    format_route(route) + "\n" +
                    format_author(route.user)
                )


async def _send_notification(bot: Bot, telegram_id: int, text: str) -> None:
    try:
        await bot.send_message(telegram_id, text, parse_mode="HTML")
    except TelegramForbiddenError:
        logger.info("Notification skipped: user %s blocked the bot", telegram_id)