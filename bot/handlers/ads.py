"""
FSM: Подача объявления пользователем (ads).
1. Описание
2. Откуда (распознавание города и страны)
3. Куда (аналогично)
4. Дата (до какой даты актуально — в формате ДД.ММ.ГГГГ)
5. Цена
Сохраняется в таблицу ads.
"""

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
import asyncio

from bot.states.ads import AdForm
from bot.database.models import Ad
from bot.database.db import SessionLocal
from bot.keyboards.inline import ad_inline_keyboard
from bot.constants import WARNING_TEXT
from bot.utils import (
    get_user_or_reply,
    get_location_or_reply,
    validate_date_input,
    format_ad,
    notify_about_new_ad,
    validate_text
)

router = Router()

@router.message(F.text == "📦 Хочу отправить")
async def start_ads(message: types.Message, state: FSMContext):
    """
    Старт FSM: спрашиваем, детали посылки.
    """
    await state.clear()
    await message.answer("Что вы хотите отправить?") #, reply_markup=ReplyKeyboardRemove())
    await state.set_state(AdForm.description)


@router.message(AdForm.description)
async def input_description(message: types.Message, state: FSMContext):
    """
    Получает описание посылки от пользователя.
    """
    if not await validate_text(message, message.text):
        return
    
    await state.update_data(description=message.text)
    await message.answer("Откуда будет отправка?\n\nПример: <code>\"Город, Страна\"</code>", parse_mode="HTML")
    await state.set_state(AdForm.from_location)


@router.message(AdForm.from_location)
async def input_from_location(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод места отправки. Распознаёт город и страну.
    """
    result = await get_location_or_reply(message)
    if not result:
        return
    city, country = result

    await state.update_data(from_city=city, from_country=country)
    await message.answer("Куда нужно доставить?\n\nПример: <code>\"Город, Страна\"</code>", parse_mode="HTML")
    await state.set_state(AdForm.to_location)


@router.message(AdForm.to_location)
async def input_to_location(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод места назначения. Распознаёт город и страну.
    """
    result = await get_location_or_reply(message)
    if not result:
        return
    city, country = result

    await state.update_data(to_city=city, to_country=country)
    await message.answer(
        "📅 До какой даты будет актуально это объявление?\n"
        "Введите дату в формате <code>ДД.ММ.ГГГГ</code>",
        parse_mode="HTML"
    )
    await state.set_state(AdForm.approx_date)


@router.message(AdForm.approx_date)
async def input_date(message: types.Message, state: FSMContext):
    """
    Получает дату в формате ДД.ММ.ГГГГ и проверяет её корректность.
    """
    ok, result = validate_date_input(message.text)
    if not ok:
        await message.answer(result, parse_mode="HTML")
        return

    await state.update_data(approx_date=result)
    await message.answer("💵 Укажите цену за доставку в $ :")
    await state.set_state(AdForm.price)


@router.message(AdForm.price)
async def input_price(message: types.Message, state: FSMContext):
    """
    Финальный шаг. Получает цену, сохраняет объявление в БД.
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
        new_ad = Ad(
            user_id=user.id,
            description=data["description"],
            from_city=data["from_city"],
            from_country=data["from_country"],
            to_city=data["to_city"],
            to_country=data["to_country"],
            approx_date=data["approx_date"],
            price=data["price"]
        )
        session.add(new_ad)
        await session.commit()

        # Обязательно обновить объект, чтобы подтянулся new_ad.user
        await session.refresh(new_ad, attribute_names=["user"])

        # ✉️ Показываем добавленное объявление
        await message.answer("Вот как выглядит ваше объявление:")
        await message.answer(format_ad(new_ad) + WARNING_TEXT, reply_markup=ad_inline_keyboard(new_ad.id), parse_mode="HTML")

        # Отправляем уведомление пользователю с похожим маршрутом
        await asyncio.sleep(2)
        await notify_about_new_ad(message.bot, new_ad.id)


    await message.answer("✅ Объявление добавлено!") #,reply_markup=main_menu(is_admin=await IsAdmin()(message)))
    await state.clear()