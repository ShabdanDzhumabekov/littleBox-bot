"""
📨 feedback.py — Хендлеры для работы с отзывами пользователей

Функции:
- Кнопка "✉️ Оставить отзыв" → бот предлагает ввести сообщение
- Сохраняет отзыв в таблицу `feedbacks`
- Админ может получить список последних отзывов через команду `/feedbacks`

Используется в главном меню
"""

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from html import escape as quote_html
from sqlalchemy import select

from bot.database.db import get_session
from bot.database.models import Feedback, User

router = Router()

# 🔐 Telegram ID администратора
ADMIN_ID = 433288212


# 🚦 Состояние для FSM — пользователь пишет отзыв
class FeedbackForm(StatesGroup):
    writing = State()


@router.message(F.text == "💬 Оставить отзыв")
async def ask_feedback(message: types.Message, state: FSMContext):
    """
    Старт ввода отзыва. Предлагаем пользователю ввести текст.
    """
    await message.answer("📝 Напишите свой отзыв, мы обязательно прочитаем!")
    await state.set_state(FeedbackForm.writing)


@router.message(FeedbackForm.writing)
async def save_feedback(message: types.Message, state: FSMContext):
    """
    Сохраняет отзыв пользователя в базу данных.
    """
    text = message.text.strip()
    telegram_id = message.from_user.id

    async for session in get_session():
        stmt = select(User).where(User.telegram_id == telegram_id)
        user = (await session.execute(stmt)).scalar_one_or_none()

        if not user:
            await message.answer("❗ Вы не зарегистрированы. Нажмите /start.")
            return

        feedback = Feedback(user_id=user.id, text=text)
        session.add(feedback)
        await session.commit()

        await message.answer("✅ Спасибо за отзыв!")

    await state.clear()


@router.message(Command("feedbacks"))
async def show_feedbacks(message: types.Message):
    """
    Только для администратора.
    Показывает 5 последних отзывов с username, датой и текстом.
    """
    if message.from_user.id != ADMIN_ID:
        return  # Игнорируем чужие вызовы

    async for session in get_session():
        stmt = select(Feedback, User).join(User).order_by(Feedback.id.desc()).limit(5)
        result = await session.execute(stmt)
        feedbacks = result.all()

        if not feedbacks:
            await message.answer("😔 Пока нет отзывов.")
            return

        for fb, user in feedbacks:
            text = (
                f"📝 <b>Отзыв от @{user.username or 'Без username'}</b>\n"
                f"🗓 {fb.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
                f"{quote_html(fb.text)}"
            )
            await message.answer(text, parse_mode="HTML")