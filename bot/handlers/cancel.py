"""
🚫 cancel.py — Хендлер команды /cancel

Функции:
- Сбрасывает текущее состояние (FSMContext)
- Возвращает пользователя в главное меню
- Используется, когда пользователь хочет выйти из текущего действия

Интеграция:
- Подключается в setup_routers()
- Рекомендуется добавить кнопку "🚫 Отмена" в UI для запуска этой команды
"""

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from bot.keyboards.menu import main_menu
from bot.filters.is_admin import IsAdmin

router = Router()

@router.message(Command("cancel"))
@router.message(F.text == "🏠 Главное меню")
async def cancel_command(message: types.Message, state: FSMContext):
    """
    Обрабатывает команду /cancel:
    - Сбрасывает состояние пользователя
    - Возвращает главное меню

    :param message: Объект сообщения от пользователя
    :param state: Контекст состояния пользователя (FSM)
    """
    await state.clear()
    await message.answer(
        "🏠 Вы вернулись в главное меню.",
        reply_markup=main_menu(is_admin=await IsAdmin()(message))
    )