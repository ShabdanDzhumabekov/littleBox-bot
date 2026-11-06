"""
Обработка ожидаемых ошибок внешних сервисов, чтобы пользователь получил ответ,
а шаг анкеты остался прежним и его можно было повторить.
"""

import logging

from aiogram import Router, F
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent, Message

from bot.utils.location import GeocodingUnavailableError

logger = logging.getLogger(__name__)

router = Router()


@router.error(ExceptionTypeFilter(GeocodingUnavailableError), F.update.message.as_("message"))
async def report_geocoding_unavailable(event: ErrorEvent, message: Message):
    logger.warning("Geocoding unavailable: %r", event.exception.__cause__)
    await message.answer("🌐 Временная ошибка при определении города. Попробуйте ещё раз.")
