"""
Обработчик команды /start:
- Регистрирует пользователя в БД
- Отправляет приветствие
- Показывает главное меню (если админ — добавляет кнопку "🛠 Админ-панель")
"""

from aiogram import Router, types
from aiogram.filters import CommandStart
from bot.keyboards.menu import main_menu
from bot.database.models import User
from bot.database.db import get_session
from sqlalchemy import select
from datetime import date

from bot.filters.is_admin import ADMIN_ID  # ← импортируем admin ID из фильтра

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    """
    Регистрирует пользователя и показывает приветственное сообщение.
    """
    telegram_id = message.from_user.id
    username = message.from_user.username
    today = date.today()

    is_admin = telegram_id == ADMIN_ID

    async for session in get_session():
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            new_user = User(
                telegram_id=telegram_id,
                username=username,
                created_at=today
            )
            session.add(new_user)
            await session.commit()
            print(f"✅ New user registered: {telegram_id}")
        else:
            print(f"👤 Existing user: {telegram_id}")

    await message.answer(
        f"👋 Привет, {username or 'гость'}! Добро пожаловать в <b>LittleBox</b> 📦\n\n"
        "🔹 <b>Здесь ты можешь:</b>\n"
        "• Отправить или получить посылку\n"
        "• Разместить маршрут путешествия\n"
        "• Найти подходящего попутчика или посылку\n"
        "• Управлять своими объявлениями\n\n"
        "⬇️ Используй кнопки внизу для начала!",
        reply_markup=main_menu(is_admin),
        parse_mode="HTML"
    )