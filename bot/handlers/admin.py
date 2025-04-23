"""
🛠 admin.py — Обработчики для админской панели

Функции:
- Обработка кнопки "🛠 Админ-панель"
- Переход на главное меню
"""

from aiogram import Router, types, F
from aiogram.filters import Command
from bot.filters.is_admin import IsAdmin
from bot.keyboards.admin_menu import admin_keyboard
from bot.keyboards.menu import main_menu

router = Router()

@router.message(F.text == "🛠 Админ-панель")
@router.message(Command("admin"))
async def open_admin_panel(message: types.Message):
    """
    Показывает клавиатуру админ-панели, если пользователь — админ.
    """
    if not await IsAdmin()(message):
        return
    await message.answer("🛠 Добро пожаловать в админ-панель!", reply_markup=admin_keyboard)

@router.message(F.text == "🔙 Назад")
async def return_to_main_menu(message: types.Message):
    """
    Возвращает обычное главное меню.
    """
    await message.answer("🔙 Главное меню", reply_markup=main_menu(is_admin=await IsAdmin()(message)))