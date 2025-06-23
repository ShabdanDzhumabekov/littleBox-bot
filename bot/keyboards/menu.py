"""
Формирование главного меню бота.
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu(is_admin: bool = False) -> ReplyKeyboardMarkup:
    """
    Главное меню. Если пользователь — админ, добавляет кнопку "🛠 Админ-панель".

    :param is_admin: Является ли пользователь администратором
    :return: Объект ReplyKeyboardMarkup
    """
    keyboard = [
        [KeyboardButton(text="📦 Хочу отправить")],
        [KeyboardButton(text="🛫 Я лечу (маршрут)")],
        [KeyboardButton(text="🔍 Найти путешественника")],
        [KeyboardButton(text="🔍 Найти посылку")],
        [KeyboardButton(text="📋 Мои объявления")],
        [KeyboardButton(text="💬 Оставить отзыв")],
        [KeyboardButton(text="📌 Безопасность")],
        [KeyboardButton(text="🏠 Главное меню")]
    ]

    if is_admin:
        keyboard.append([KeyboardButton(text="🛠 Админ-панель")])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, is_persistent=True)