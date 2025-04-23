"""
FSM: Подача маршрута путешественником (routes).
1. Откуда (распознаётся город и страна)
2. Куда (аналогично)
3. Когда (дата в формате ДД.ММ.ГГГГ)
4. Что может взять
5. Условия
Сохраняется в таблицу routes.
"""

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from sqlalchemy import select

from bot.states.route import RouteForm
from bot.database.models import Route
from bot.database.db import get_session
from bot.keyboards.menu import main_menu
from bot.utils import get_location_or_reply, get_user_or_reply, validate_date_input

router = Router()

@router.message(F.text == "🛫 Я лечу (маршрут)")
async def start_route(message: types.Message, state: FSMContext):
    """
    Старт FSM: спрашиваем, откуда пользователь вылетает.
    """
    await message.answer("Откуда вы летите?\n\nПример: <code>Город, Страна</code>", parse_mode="HTML")
    await state.set_state(RouteForm.from_location)


@router.message(RouteForm.from_location)
async def set_from_location(message: types.Message, state: FSMContext):
    """
    Обработка места отправления.
    """
    result = await get_location_or_reply(message)
    if not result:
        return
    city, country = result

    await state.update_data(from_city=city, from_country=country)
    await message.answer("Куда вы летите?\n\nПример: <code>Город, Страна</code>", parse_mode="HTML")
    await state.set_state(RouteForm.to_location)


@router.message(RouteForm.to_location)
async def set_to_location(message: types.Message, state: FSMContext):
    """
    Обработка места назначения.
    """
    result = await get_location_or_reply(message)
    if not result:
        return
    city, country = result

    await state.update_data(to_city=city, to_country=country)
    await message.answer("📅 Когда у вас рейс?\nВведите дату в формате <code>ДД.ММ.ГГГГ</code>", parse_mode="HTML")
    await state.set_state(RouteForm.travel_date)


@router.message(RouteForm.travel_date)
async def set_travel_date(message: types.Message, state: FSMContext):
    """
    Обработка даты рейса.
    """
    ok, result = validate_date_input(message.text)
    if not ok:
        await message.answer(result, parse_mode="HTML")
        return

    await state.update_data(travel_date=result)
    await message.answer("🧳 Что вы можете взять с собой?\n(например: до 2 кг, маленький пакет)")
    await state.set_state(RouteForm.luggage)


@router.message(RouteForm.luggage)
async def set_luggage(message: types.Message, state: FSMContext):
    """
    Обработка ввода багажа.
    """
    await state.update_data(luggage=message.text)
    await message.answer("💬 Укажите дополнительные условия (или просто '—'):")
    await state.set_state(RouteForm.conditions)


@router.message(RouteForm.conditions)
async def finish_route(message: types.Message, state: FSMContext):
    """
    Финальный шаг — сохранение маршрута в БД.
    """
    await state.update_data(conditions=message.text)
    data = await state.get_data()
    telegram_id = message.from_user.id

    user = await get_user_or_reply(telegram_id, message)
    if not user:
        return

    async for session in get_session():
        new_route = Route(
            user_id=user.id,
            from_city=data["from_city"],
            from_country=data["from_country"],
            to_city=data["to_city"],
            to_country=data["to_country"],
            travel_date=data["travel_date"],
            luggage=data["luggage"],
            conditions=data["conditions"]
        )
        session.add(new_route)
        await session.commit()

    await message.answer("✅ Маршрут добавлен! Спасибо!", reply_markup=main_menu())
    await state.clear()