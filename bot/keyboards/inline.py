"""
🧩 inline.py — Генерация inline-кнопок для объявлений и маршрутов.

Содержит:
- ad_inline_keyboard(ad_id) — кнопки для объявления (редактировать / удалить)
- route_inline_keyboard(route_id) — кнопки для маршрута (редактировать / удалить)
- contact_ad_keyboard(ad_id) — кнопка «Связаться» под чужим объявлением
- contact_route_keyboard(route_id) — кнопка «Связаться» под чужим маршрутом
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def ad_inline_keyboard(ad_id: int) -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру для объявления (Ad)

    :param ad_id: ID объявления
    :return: InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✏️ Редактировать", callback_data=f"edit_ad_{ad_id}"),
                InlineKeyboardButton(text="❌ Удалить", callback_data=f"delete_ad_{ad_id}")
            ]
        ]
    )


def route_inline_keyboard(route_id: int) -> InlineKeyboardMarkup:
    """
    Возвращает клавиатуру для маршрута (Route)

    :param route_id: ID маршрута
    :return: InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✏️ Редактировать", callback_data=f"edit_route_{route_id}"),
                InlineKeyboardButton(text="❌ Удалить", callback_data=f"delete_route_{route_id}")
            ]
        ]
    )


def contact_ad_keyboard(ad_id: int) -> InlineKeyboardMarkup:
    """
    Возвращает кнопку «Связаться» для объявления, автор которого скрыл username

    :param ad_id: ID объявления
    :return: InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✉️ Связаться с автором", callback_data=f"contact_ad_{ad_id}")]
        ]
    )


def contact_route_keyboard(route_id: int) -> InlineKeyboardMarkup:
    """
    Возвращает кнопку «Связаться» для маршрута, автор которого скрыл username

    :param route_id: ID маршрута
    :return: InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✉️ Связаться с автором", callback_data=f"contact_route_{route_id}")]
        ]
    )