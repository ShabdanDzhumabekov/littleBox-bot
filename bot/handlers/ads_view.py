"""
Хендлер: 🔍 Найти посылку
Бот спрашивает точное направление и показывает подходящие объявления (ads).
Совпадения должны быть полными по откуда и куда.
"""

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from bot.states.ads_view import FindAdForm
from bot.filters import IsFreeText
from bot.utils.location import parse_location
from sqlalchemy import select
from datetime import datetime
from bot.database.db import SessionLocal
from bot.database.models import Ad, User
from bot.utils.formatters import format_ad, format_author

router = Router()

@router.message(F.text == "🔍 Найти посылку")
async def start_find_ad(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("📍 Из какого города и страны будет отправка?\n\nПример: <code>\"Город, Страна\"</code>", parse_mode="HTML")
    await state.set_state(FindAdForm.from_location)

@router.message(FindAdForm.from_location, IsFreeText())
async def input_from_location(message: types.Message, state: FSMContext):
    city, country = await parse_location(message.text)

    if not country:
        await message.answer("❗ Не удалось определить точку отправки. Пример: <code>Бишкек, Кыргызстан</code>", parse_mode="HTML")
        return

    await state.update_data(from_city=city, from_country=country)
    await message.answer("📦 Куда нужно доставить?\n\nПример: <code>\"Город, Страна\"</code>", parse_mode="HTML")
    await state.set_state(FindAdForm.to_location)

@router.message(FindAdForm.to_location, IsFreeText())
async def input_to_location(message: types.Message, state: FSMContext):
    to_city, to_country = await parse_location(message.text)

    if not to_country:
        await message.answer("❗ Не удалось определить точку назначения. Пример: <code>\"Белград, Сербия\"</code>", parse_mode="HTML")
        return

    data = await state.get_data()

    async with SessionLocal() as session:
        stmt = select(Ad, User).join(User).where(
            Ad.from_city == data["from_city"],
            Ad.from_country == data["from_country"],
            Ad.to_city == to_city,
            Ad.to_country == to_country,
            Ad.approx_date >= datetime.now().date()
        ).order_by(Ad.approx_date.asc())

        result = await session.execute(stmt)
        ads = result.all()

        if not ads:
            await message.answer("😔 Нет объявлений с таким маршрутом.")
            await state.clear()
            return
        
        await message.answer(f"📦 Найдено: {len(ads)} объявлений")

        for ad, user in ads:
            text = format_ad(ad) + "\n" + format_author(user)
            await message.answer(text, parse_mode="HTML")

    await state.clear()