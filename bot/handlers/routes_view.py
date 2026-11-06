"""
Хендлер: 🔍 Найти путешественника
Пошагово спрашивает откуда и куда, фильтрует маршруты.
Логика:
— Показывает маршруты, где to_city и to_country совпадают
— Сначала фильтрует по from_city + from_country
— Если таких нет, фильтрует по from_country
"""

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from bot.states.routes_view import FindRouteForm
from bot.filters import IsFreeText
from bot.utils.location import parse_location
from sqlalchemy import select
from datetime import datetime
from bot.database.db import SessionLocal
from bot.database.models import Route, User
from bot.utils.formatters import format_route

router = Router()

# 🔹 Шаг 1 — пользователь нажал "🔍 Найти путешественника"
@router.message(F.text == "🔍 Найти путешественника")
async def start_find_route(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("📍 Откуда вы хотите отправить посылку?\n\nПример: <code>\"Город, Страна\"</code>", parse_mode="HTML")
    await state.set_state(FindRouteForm.from_location)

# 🔹 Шаг 2 — ввод "откуда"
@router.message(FindRouteForm.from_location, IsFreeText())
async def input_from_location(message: types.Message, state: FSMContext):
    city, country = await parse_location(message.text)

    if not country:
        await message.answer("❗ Не удалось определить местоположение. Пример: <code>\"Бишкек, Кыргызстан\"</code>", parse_mode="HTML")
        return

    await state.update_data(from_city=city, from_country=country)
    await message.answer("📦 Куда нужно доставить?\n\nПример: <code>\"Город, Страна\"</code>", parse_mode="HTML")
    await state.set_state(FindRouteForm.to_location)

# 🔹 Шаг 3 — ввод "куда" + фильтрация маршрутов
@router.message(FindRouteForm.to_location, IsFreeText())
async def input_to_location(message: types.Message, state: FSMContext):
    to_city, to_country = await parse_location(message.text)

    if not to_country:
        await message.answer("❗ Не удалось определить место назначения. Пример: <code>\"Белград, Сербия\"</code>", parse_mode="HTML")
        return

    data = await state.get_data()
    from_city = data.get("from_city")
    from_country = data.get("from_country")

    async with SessionLocal() as session:
        # 1. Фильтруем маршруты по месту назначения (обязательно)
        stmt = select(Route, User).join(User).where(
            Route.to_country == to_country,
            Route.travel_date >= datetime.now().date()
        ).order_by(Route.travel_date.asc())
        if to_city:
            stmt = stmt.where(Route.to_city == to_city).order_by(Route.travel_date.asc())

        result = await session.execute(stmt)
        all_routes = result.all()

        if not all_routes:
            await message.answer("😔 Пока нет маршрутов в это направление.")
            await state.clear()
            return

        # 2. Разбиваем на две группы
        exact_matches = []
        fallback_matches = []

        for route, user in all_routes:
            if route.from_city == from_city and route.from_country == from_country:
                exact_matches.append((route, user))
            elif route.from_country == from_country:
                fallback_matches.append((route, user))

        routes_to_show = exact_matches or fallback_matches

        if not routes_to_show:
            await message.answer("😔 Нет подходящих маршрутов из нужной страны.")
            await state.clear()
            return
        
        await message.answer(f"🛫 Найдено: {len(routes_to_show)} маршрутов")

        for route, user in routes_to_show:
            text = format_route(route) + f"\n👤 @{user.username or 'Без username'}"
            await message.answer(text, parse_mode="HTML")

    await state.clear()