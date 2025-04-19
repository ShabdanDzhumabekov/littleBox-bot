"""
Формирование главного меню бота.
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    keyboard = [
        [KeyboardButton(text="📦 Разместить объявление")],
        [KeyboardButton(text="🛫 Я лечу (маршрут)")],
        [KeyboardButton(text="🔍 Найти путешественника")],
        [KeyboardButton(text="🔍 Найти посылку")],
        [KeyboardButton(text="📋 Мои объявления")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)