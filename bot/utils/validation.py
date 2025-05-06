"""
validation.py — Утилиты для валидации текстового ввода в FSM
"""

from aiogram.types import Message
from bot.constants import MAX_DESCRIPTION_LENGTH


async def validate_text(message: Message, text: str, max_length: int = MAX_DESCRIPTION_LENGTH) -> bool:
    """
    Проверяет, не превышает ли текст указанную длину.
    При превышении выводит сообщение об ошибке.

    :param message: объект сообщения от пользователя
    :param text: текст, введённый пользователем
    :param max_length: максимальная длина текста
    :return: True, если текст корректен, иначе False
    """
    if len(text) > max_length:
        await message.answer(f"❗️Текст слишком длинный. Максимум {max_length} символов.")
        return False
    return True