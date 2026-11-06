"""
Утилиты для определения города и страны по введённому пользователем адресу.
Работают через Nominatim (OpenStreetMap).
"""

import asyncio

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError
from aiogram.types import Message

# Инициализация геокодера
geolocator = Nominatim(user_agent="littleBox")


class GeocodingUnavailableError(Exception):
    """Nominatim не ответил: таймаут, лимит запросов или сервис недоступен."""


async def parse_location(text: str):
    """
    Извлекает город и страну из текста.

    :param text: Строка вида "Москва, Россия"
    :return: (город, страна) или (None, None)
    :raises GeocodingUnavailableError: если Nominatim не ответил
    """
    try:
        location = await asyncio.to_thread(
            geolocator.geocode, text, addressdetails=True, language="ru", timeout=5
        )
    except GeocoderServiceError as error:
        raise GeocodingUnavailableError from error

    if not location:
        return None, None

    address = location.raw.get("address", {})
    city = (
        address.get("city") or
        address.get("town") or
        address.get("village") or
        address.get("municipality") or
        address.get("state")
    )
    country = address.get("country")

    return city, country


async def get_location_or_reply(message: Message):
    """
    Определяет местоположение и отвечает ошибкой, если не удалось.

    :param message: Сообщение пользователя
    :return: (город, страна) или None
    """
    city, country = await parse_location(message.text)
    
    if not city or not country:
        await message.answer(
            "❗️Не удалось определить город и страну. Пример: <code>Город, Страна</code>",
            parse_mode="HTML"
        )
        return None
    
    return city, country