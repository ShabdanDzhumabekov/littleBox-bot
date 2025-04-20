"""
FSM: Подача маршрута путешественником.
Сценарий:
1. Откуда вы летите?
2. Куда летите?
3. Когда?
4. Что можете взять с собой?
5. Условия/комментарии

Сохраняется в таблицу routes.
"""

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from bot.states.route import RouteForm
from bot.database.models import Route, User
from bot.database.db import get_session
from sqlalchemy import select
from datetime import datetime

router = Router()

# 🔹 Старт FSM: кнопка "Я лечу"
@router.message(F.text == "🛫 Я лечу (маршрут)")
async def start_route(message: types.Message, state: FSMContext):
    await message.answer("Откуда вы летите?")
    await state.set_state(RouteForm.from_location)

# 🔹 Шаг 1: откуда
@router.message(RouteForm.from_location)
async def set_from(message: types.Message, state: FSMContext):
    await state.update_data(from_location=message.text)
    await message.answer("Куда летите?")
    await state.set_state(RouteForm.to_location)

# 🔹 Шаг 2: куда
@router.message(RouteForm.to_location)
async def set_to(message: types.Message, state: FSMContext):
    await state.update_data(to_location=message.text)
    await message.answer("Когда планируете поездку?\nПожалуйста, введите дату в формате ДД.ММ.ГГГГ (например, 05.06.2025)")
    await state.set_state(RouteForm.travel_date)

# 🔹 Шаг 3: дата (Date)
@router.message(RouteForm.travel_date)
async def set_date(message: types.Message, state: FSMContext):
    user_input = message.text.strip()
    try:
        travel_date = datetime.strptime(user_input, "%d.%m.%Y").date()
    except ValueError:
        await message.answer("Пожалуйста, введите дату в формате ДД.ММ.ГГГГ (например, 05.06.2025)")
        return

    await state.update_data(travel_date=travel_date)
    await message.answer("Что вы можете взять с собой?")
    await state.set_state(RouteForm.luggage)

# 🔹 Шаг 4: багаж
@router.message(RouteForm.luggage)
async def set_luggage(message: types.Message, state: FSMContext):
    await state.update_data(luggage=message.text)
    await message.answer("Условия или комментарии?")
    await state.set_state(RouteForm.conditions)

# 🔹 Финальный шаг: комментарии + сохранение
@router.message(RouteForm.conditions)
async def set_conditions(message: types.Message, state: FSMContext):
    await state.update_data(conditions=message.text)
    data = await state.get_data()
    telegram_id = message.from_user.id

    async for session in get_session():
        # Получаем пользователя
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            await message.answer("❗ Пожалуйста, сначала введите /start.")
            return

        new_route = Route(
            user_id=user.id,
            from_location=data["from_location"],
            to_location=data["to_location"],
            travel_date=data["travel_date"],
            luggage=data["luggage"],
            conditions=data["conditions"]
        )
        session.add(new_route)
        await session.commit()

    await message.answer("✅ Ваш маршрут сохранён. Спасибо!", reply_markup=ReplyKeyboardRemove())
    await state.clear()