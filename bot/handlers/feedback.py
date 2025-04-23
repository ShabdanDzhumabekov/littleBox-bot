"""
feedback.py — Оставить отзыв

Пользователь может отправить отзыв, который сохраняется в таблицу Feedback.
"""

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy import select

from bot.database.db import get_session
from bot.database.models import Feedback, User

router = Router()


# 🚦 Состояние FSM
class FeedbackForm(StatesGroup):
    writing = State()


@router.message(F.text == "✉️ Оставить отзыв")
async def ask_feedback(message: types.Message, state: FSMContext):
    """
    Старт: пользователь хочет оставить отзыв
    """
    await message.answer("📝 Напишите свой отзыв, мы обязательно прочитаем!")
    await state.set_state(FeedbackForm.writing)


@router.message(FeedbackForm.writing)
async def save_feedback(message: types.Message, state: FSMContext):
    """
    Сохраняет отзыв в базу данных
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