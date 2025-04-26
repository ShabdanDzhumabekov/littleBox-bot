"""
📦 formatters.py — Утилиты для форматирования объявлений и маршрутов

Содержит шаблонные функции:
- format_ad(ad) — возвращает отформатированное описание объявления
- format_route(route) — возвращает отформатированное описание маршрута
"""

from bot.database.models import Ad, Route


def format_ad(ad: Ad) -> str:
    """
    Возвращает отформатированное описание объявления (Ad) для отображения в Telegram.

    :param ad: Объект объявления
    :return: Строка с HTML-разметкой
    """
    return (
        f"📝 <i>{ad.description}</i>\n"
        f"🌍 {ad.from_city}, {ad.from_country} ➡️ {ad.to_city}, {ad.to_country}\n"
        f"📅 Актуально до: {ad.approx_date.strftime('%d.%m.%Y')}\n"
        f"💵 {ad.price}$"
    )


def format_route(route: Route) -> str:
    """
    Возвращает отформатированное описание маршрута (Route) для отображения в Telegram.

    :param route: Объект маршрута
    :return: Строка с HTML-разметкой
    """
    return (
        f"🛫 <b>Маршрут</b>\n"
        f"🌍 {route.from_city}, {route.from_country} ➡️ {route.to_city}, {route.to_country}\n"
        f"📅 {route.travel_date.strftime('%d.%m.%Y')}\n"
        f"🧳 {route.luggage}\n"
        f"💬 {route.conditions or '—'}"
    )