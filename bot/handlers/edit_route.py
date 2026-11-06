"""
Редактирование маршрута пользователя (Route) через FSM.
"""

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from bot.database.db import SessionLocal
from bot.database.models import Route, User
from bot.states.edit_route import EditRouteForm
from bot.filters import IsFreeText
from bot.keyboards.inline import route_inline_keyboard
from bot.utils import (
    get_location_or_reply,
    get_user_or_reply,
    validate_date_input,
    format_route,
    validate_text
)

router = Router()


@router.callback_query(lambda c: c.data.startswith("edit_route_"))
async def start_edit_route(callback: types.CallbackQuery, state: FSMContext):
    """
    Старт редактирования маршрута — спрашиваем новое место отправления.
    """
    route_id = int(callback.data.split("_")[-1])
    telegram_id = callback.from_user.id

    async with SessionLocal() as session:
        stmt_route = select(Route).join(User).where(Route.id == route_id, User.telegram_id == telegram_id)
        route = (await session.execute(stmt_route)).scalar_one_or_none()

        if not route:
            await callback.answer("❌ Маршрут не найден или не ваш", show_alert=True)
            return

        await state.update_data(route_id=route.id)
        await callback.message.answer("✏️ Введите новое место отправления (Город, Страна):")
        await state.set_state(EditRouteForm.from_location)


@router.message(EditRouteForm.from_location, IsFreeText())
async def edit_from_location(message: types.Message, state: FSMContext):
    result = await get_location_or_reply(message)
    if not result:
        return
    city, country = result

    await state.update_data(from_city=city, from_country=country)
    await message.answer("🌍 Введите новое место назначения (Город, Страна):")
    await state.set_state(EditRouteForm.to_location)


@router.message(EditRouteForm.to_location, IsFreeText())
async def edit_to_location(message: types.Message, state: FSMContext):
    result = await get_location_or_reply(message)
    if not result:
        return
    city, country = result

    await state.update_data(to_city=city, to_country=country)
    await message.answer("📅 Введите дату отправления в формате <code>ДД.ММ.ГГГГ</code>", parse_mode="HTML")
    await state.set_state(EditRouteForm.travel_date)


@router.message(EditRouteForm.travel_date, IsFreeText())
async def edit_date(message: types.Message, state: FSMContext):
    ok, result = validate_date_input(message.text)
    if not ok:
        await message.answer(result, parse_mode="HTML")
        return

    await state.update_data(travel_date=result)
    await message.answer("🧳 Что вы можете взять с собой?\n(например: до 2 кг, маленький пакет)")
    await state.set_state(EditRouteForm.luggage)


@router.message(EditRouteForm.luggage, IsFreeText())
async def edit_luggage(message: types.Message, state: FSMContext):
    if not await validate_text(message, message.text):
        return
    
    await state.update_data(luggage=message.text)
    await message.answer("💬 Укажите дополнительные условия (или '—'):")
    await state.set_state(EditRouteForm.conditions)


@router.message(EditRouteForm.conditions, IsFreeText())
async def finish_edit(message: types.Message, state: FSMContext):
    """
    Финальное обновление маршрута в базе данных.
    """
    if not await validate_text(message, message.text):
        return
    
    await state.update_data(conditions=message.text)
    data = await state.get_data()
    telegram_id = message.from_user.id

    user = await get_user_or_reply(telegram_id, message)
    if not user:
        return

    async with SessionLocal() as session:
        stmt_route = select(Route).where(Route.id == data["route_id"], Route.user_id == user.id)
        route = (await session.execute(stmt_route)).scalar_one_or_none()

        if not route:
            await message.answer("❗ Маршрут не найден или не ваш.")
            await state.clear()
            return

        route.from_city = data["from_city"]
        route.from_country = data["from_country"]
        route.to_city = data["to_city"]
        route.to_country = data["to_country"]
        route.travel_date = data["travel_date"]
        route.luggage = data["luggage"]
        route.conditions = data["conditions"]

        await session.commit()

        await message.answer("Вот как выглядит ваш маршрут после редактирования:")
        await message.answer(format_route(route), reply_markup=route_inline_keyboard(route.id), parse_mode="HTML")

    await message.answer("✅ Маршрут успешно обновлён!")
    await state.clear()