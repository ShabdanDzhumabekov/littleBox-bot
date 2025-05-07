"""
🛠 admin_menu.py — Меню администратора

Функции:
- Обработка кнопки "🛠 Админ-панель" только для администратора
- Показывает кнопки: 📊 Статистика, 💬 Отзывы, 🔙 Назад
"""

from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()

# Админское меню
admin_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="💬 Отзывы")],
        [KeyboardButton(text="🔙 Назад")]
    ],
    resize_keyboard=True
)