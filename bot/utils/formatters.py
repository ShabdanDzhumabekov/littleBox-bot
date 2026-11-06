"""
📦 formatters.py — Утилиты для форматирования объявлений и маршрутов

Содержит шаблонные функции:
- format_ad(ad) — возвращает отформатированное описание объявления
- format_route(route) — возвращает отформатированное описание маршрута
"""

from aiogram import html

from bot.database.models import Ad, Route


def format_ad(ad: Ad) -> str:
    """
    Возвращает отформатированное описание объявления (Ad) для отображения в Telegram.

    :param ad: Объект объявления
    :return: Строка с HTML-разметкой
    """
    return (
        f"📝 <i>{html.quote(ad.description)}</i>\n"
        f"🌍 {html.quote(ad.from_city)}, {html.quote(ad.from_country)} ➡️ {html.quote(ad.to_city)}, {html.quote(ad.to_country)}\n"
        f"📅 Актуально до: {ad.approx_date.strftime('%d.%m.%Y')}\n"
        f"💵 {html.quote(ad.price)}$"
    )


def format_route(route: Route) -> str:
    """
    Возвращает отформатированное описание маршрута (Route) для отображения в Telegram.

    :param route: Объект маршрута
    :return: Строка с HTML-разметкой
    """
    return (
        f"🛫 <b>Маршрут</b>\n"
        f"🌍 {html.quote(route.from_city)}, {html.quote(route.from_country)} ➡️ {html.quote(route.to_city)}, {html.quote(route.to_country)}\n"
        f"📅 {route.travel_date.strftime('%d.%m.%Y')}\n"
        f"🧳 {html.quote(route.luggage)}\n"
        f"💬 {html.quote(route.conditions or '—')}"
    )