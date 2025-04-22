"""
Утилиты для получения пользователей из базы данных по Telegram ID.
"""

from sqlalchemy import select
from bot.database.db import get_session
from bot.database.models import User


async def get_user_or_reply(telegram_id: int, message):
    """
    Получает пользователя из базы данных по Telegram ID.

    :param telegram_id: ID пользователя в Telegram
    :param message: Сообщение для ответа, если пользователь не найден
    :return: User объект или None
    """
    async for session in get_session():
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            await message.answer("❗ Вы ещё не зарегистрированы. Введите /start.")
            return None

        return user