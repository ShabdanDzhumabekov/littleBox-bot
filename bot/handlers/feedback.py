"""
📨 feedback.py — Хендлеры для работы с отзывами пользователей

Функции:
- Кнопка "💬 Оставить отзыв" → бот предлагает ввести сообщение
- Сохраняет отзыв в таблицу `feedbacks`
- Команда /feedbacks доступна только администратору — показывает последние отзывы
"""

from aiogram import Router, types, F, html
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from sqlalchemy import select

from bot.database.db import SessionLocal
from bot.database.models import Feedback, User
from bot.filters import IsAdmin, IsFreeText
from bot.constants import MAX_FEEDBACK_LENGTH
from bot.utils import validate_text

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
    await state.clear()
    await message.answer("📝 Напишите свой отзыв, мы обязательно прочитаем!")
    await state.set_state(FeedbackForm.writing)


@router.message(FeedbackForm.writing, IsFreeText())
async def save_feedback(message: types.Message, state: FSMContext):
    """
    Сохраняет отзыв пользователя в базу данных.
    """
    if not await validate_text(message, message.text, MAX_FEEDBACK_LENGTH):
        return
    
    text = message.text.strip()
    telegram_id = message.from_user.id

    async with SessionLocal() as session:
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
@router.message(F.text == "💬 Отзывы", IsAdmin())
async def show_feedbacks(message: types.Message):
    """
    Команда доступна только администратору.
    Показывает 5 последних отзывов с датой, username и текстом.
    """
    async with SessionLocal() as session:
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
                f"{html.quote(fb.text)}"
            )
            await message.answer(text, parse_mode="HTML")