"""
Обработчик команды /start:
- Регистрирует пользователя в БД
- Отправляет приветствие
- Показывает главное меню
"""

from aiogram import Router, types
from aiogram.filters import CommandStart
from bot.keyboards.menu import main_menu
from bot.database.models import User
from bot.database.db import get_session
from sqlalchemy import select
from datetime import date

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    telegram_id = message.from_user.id
    username = message.from_user.username
    today = date.today()

    async for session in get_session():
        # Проверяем: есть ли уже такой пользователь
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            # Создаём нового пользователя
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

    # Отправляем сообщение пользователю
    await message.answer(
        f"👋 Привет, {username or 'гость'}! Добро пожаловать в LittleBox!\n"
        "📦 Ты можешь отправить посылку или предложить маршрут.",
        reply_markup=main_menu()
    )