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
from bot.database.db import SessionLocal
from bot.filters.is_admin import IsAdmin
from sqlalchemy import select
from datetime import date

#from bot.filters.is_admin import ADMIN_ID  # ← импортируем admin ID из фильтра

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    """
    Регистрирует пользователя и показывает приветственное сообщение.
    """
    telegram_id = message.from_user.id
    username = message.from_user.username
    today = date.today()

    async with SessionLocal() as session:
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

            # Отправляем предупреждение, если username отсутствует
            if not username:
                await message.answer(
                    "⚠️ У тебя скрыт username в Telegram.\n\n"
                    "Если кто-то захочет с тобой связаться через LittleBox, "
                    "мы пришлем тебе его username, чтобы ты мог ответить.\n\n"
                    "Ты можешь открыть username в настройках Telegram, чтобы другим было проще с тобой связаться."
                )
        else:
            print(f"👤 Existing user: {telegram_id}")

    await message.answer(
        f"👋 Привет, {username or 'гость'}! Добро пожаловать в <b>LittleBox</b> 📦\n\n"
        "🔹 <b>Здесь ты можешь:</b>\n"
        "• Отправить посылку\n"
        "• Разместить маршрут путешествия\n"
        "• Найти подходящего попутчика или посылку\n"
        "• Управлять своими объявлениями\n"
        "• /help — список возможностей бота \n"
        "• /rules — правила безопасности \n\n"
        "⬇️ Используй кнопки внизу чтобы начать!",
        reply_markup=main_menu(is_admin=await IsAdmin()(message)),
        parse_mode="HTML"
    )