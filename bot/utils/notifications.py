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

from aiogram import Bot
from sqlalchemy import select
from bot.database.models import Ad, Route, User
from bot.database.db import get_session
from bot.utils import format_ad, format_route


async def notify_about_new_ad(bot: Bot, ad: Ad):
    """
    Уведомляет пользователей, у которых есть подходящие маршруты под новое объявление.

    :param bot: Экземпляр Telegram-бота
    :param ad: Объект объявления (Ad), только что добавленного
    """
    async for session in get_session():
        stmt = select(Route, User).join(User).where(
            Route.from_city == ad.from_city,
            Route.from_country == ad.from_country,
            Route.to_city == ad.to_city,
            Route.to_country == ad.to_country
        )
        result = await session.execute(stmt)
        matches = result.all()

        for route, user in matches:
            # Не уведомляем автора
            if user.telegram_id != ad.user.telegram_id:
                await bot.send_message(
                    user.telegram_id,
                    "📦 Появилось новое объявление, подходящее под ваш маршрут:\n\n" +
                    format_ad(ad),
                    parse_mode="HTML"
                )


async def notify_about_new_route(bot: Bot, route: Route):
    """
    Уведомляет пользователей, у которых есть подходящие объявления под новый маршрут.

    :param bot: Экземпляр Telegram-бота
    :param route: Объект маршрута (Route), только что добавленного
    """
    async for session in get_session():
        stmt = select(Ad, User).join(User).where(
            Ad.from_city == route.from_city,
            Ad.from_country == route.from_country,
            Ad.to_city == route.to_city,
            Ad.to_country == route.to_country
        )
        result = await session.execute(stmt)
        matches = result.all()

        for ad, user in matches:
            # Не уведомляем автора
            if user.telegram_id != route.user.telegram_id:
                await bot.send_message(
                    user.telegram_id,
                    "🛫 Появился путешественник, подходящий под ваше объявление:\n\n" +
                    format_route(route),
                    parse_mode="HTML"
                )