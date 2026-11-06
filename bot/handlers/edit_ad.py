"""
Редактирование объявления пользователя (Ad) через FSM.
"""

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from bot.database.db import SessionLocal
from bot.database.models import Ad, User
from bot.states.edit_ad import EditAdForm
from bot.filters import IsFreeText
from bot.keyboards.inline import ad_inline_keyboard
from bot.utils import (
    get_location_or_reply,
    get_user_or_reply,
    validate_date_input,
    format_ad,
    validate_text
)

router = Router()


@router.callback_query(lambda c: c.data.startswith("edit_ad_"))
async def start_edit_ad(callback: types.CallbackQuery, state: FSMContext):
    """
    Старт редактирования объявления — спрашиваем новое описание.
    """
    ad_id = int(callback.data.split("_")[-1])
    telegram_id = callback.from_user.id

    async with SessionLocal() as session:
        stmt_ad = select(Ad).join(User).where(Ad.id == ad_id, User.telegram_id == telegram_id)
        ad = (await session.execute(stmt_ad)).scalar_one_or_none()

        if not ad:
            await callback.answer("❌ Объявление не найдено или не ваше", show_alert=True)
            return

        await state.update_data(ad_id=ad.id)
        await callback.message.answer("✏️ Введите новое описание посылки:")
        await state.set_state(EditAdForm.description)


@router.message(EditAdForm.description, IsFreeText())
async def edit_description(message: types.Message, state: FSMContext):
    if not await validate_text(message, message.text):
        return
    
    await state.update_data(description=message.text)
    await message.answer("🌍 Откуда будет отправка? (пример: \"Город, Страна\"):")
    await state.set_state(EditAdForm.from_location)


@router.message(EditAdForm.from_location, IsFreeText())
async def edit_from_location(message: types.Message, state: FSMContext):
    result = await get_location_or_reply(message)
    if not result:
        return
    city, country = result

    await state.update_data(from_city=city, from_country=country)
    await message.answer("🌍 Куда нужно доставить? (пример: \"Город, Страна\"):")
    await state.set_state(EditAdForm.to_location)


@router.message(EditAdForm.to_location, IsFreeText())
async def edit_to_location(message: types.Message, state: FSMContext):
    result = await get_location_or_reply(message)
    if not result:
        return
    city, country = result

    await state.update_data(to_city=city, to_country=country)
    await message.answer("📅 До какой даты будет актуально объявление? Введите в формате <code>ДД.ММ.ГГГГ</code>", parse_mode="HTML")
    await state.set_state(EditAdForm.approx_date)


@router.message(EditAdForm.approx_date, IsFreeText())
async def edit_date(message: types.Message, state: FSMContext):
    ok, result = validate_date_input(message.text)
    if not ok:
        await message.answer(result, parse_mode="HTML")
        return

    await state.update_data(approx_date=result)
    await message.answer("💵 Укажите цену за доставку:")
    await state.set_state(EditAdForm.price)


@router.message(EditAdForm.price, IsFreeText())
async def finish_edit(message: types.Message, state: FSMContext):
    """
    Финальный шаг: сохранение отредактированного объявления.
    """
    if not await validate_text(message, message.text, 10):
        return
    
    await state.update_data(price=message.text)
    data = await state.get_data()
    telegram_id = message.from_user.id

    user = await get_user_or_reply(telegram_id, message)
    if not user:
        return

    async with SessionLocal() as session:
        stmt_ad = select(Ad).where(Ad.id == data["ad_id"], Ad.user_id == user.id)
        ad = (await session.execute(stmt_ad)).scalar_one_or_none()

        if not ad:
            await message.answer("❗ Объявление не найдено или не ваше.")
            await state.clear()
            return

        ad.description = data["description"]
        ad.from_city = data["from_city"]
        ad.from_country = data["from_country"]
        ad.to_city = data["to_city"]
        ad.to_country = data["to_country"]
        ad.approx_date = data["approx_date"]
        ad.price = data["price"]

        await session.commit()

        await message.answer("Вот как выглядит ваше объявление после редактирования:")
        await message.answer(format_ad(ad), reply_markup=ad_inline_keyboard(ad.id), parse_mode="HTML")

    await message.answer("✅ Объявление обновлено!")
    await state.clear()