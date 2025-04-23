"""
📨 feedback.py — Хендлеры для работы с отзывами пользователей

Функции:
- Кнопка "💬 Оставить отзыв" → бот предлагает ввести сообщение
- Сохраняет отзыв в таблицу `feedbacks`
- Команда /feedbacks доступна только администратору — показывает последние отзывы
"""

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from sqlalchemy import select

from bot.database.db import get_session
from bot.database.models import Feedback, User
from bot.filters import IsAdmin

router = Router()


class FeedbackForm(StatesGroup):
    """
    Состояния для FSM: пользователь пишет отзыв
    """
    writing = State()


@router.message(F.text == "💬 Оставить отзыв")
async def ask_feedback(message: types.Message, state: FSMContext):
    """
    Начало ввода отзыва. Просим пользователя написать текст.
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


@router.message(Command("feedbacks"), IsAdmin())
async def show_feedbacks(message: types.Message):
    """
    Команда доступна только администратору.
    Показывает 5 последних отзывов с датой, username и текстом.
    """
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
                f"{fb.text}"
            )
            await message.answer(text, parse_mode="HTML")