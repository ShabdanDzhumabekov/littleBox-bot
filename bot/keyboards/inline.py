"""
🧩 inline.py — Генерация inline-кнопок для объявлений и маршрутов.

Содержит:
- ad_inline_keyboard(ad_id) — кнопки для объявления (редактировать / удалить)
- route_inline_keyboard(route_id) — кнопки для маршрута (редактировать / удалить)
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