"""
FSM: Подача объявления пользователем (ads).
1. Выбор типа объявления (отправка/получение)
2. Описание
3. Откуда (распознавание города и страны)
4. Куда (аналогично)
5. Дата (до какой даты актуально — в формате ДД.ММ.ГГГГ)
6. Цена
Сохраняется в таблицу ads.
"""

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from bot.states.ads import AdForm
from bot.database.models import Ad
from bot.database.db import get_session
from bot.utils import (
    get_user_or_reply,
    get_location_or_reply,
    validate_date_input,
)

router = Router()

@router.message(F.text == "📦 Разместить объявление")
async def choose_type(message: types.Message, state: FSMContext):
    """
    Старт подачи объявления.
    Показывает клавиатуру с выбором: отправить или получить посылку.
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📤 Отправить"), KeyboardButton(text="📥 Получить")]],
        resize_keyboard=True
    )
    await message.answer("Вы хотите отправить или получить посылку?", reply_markup=keyboard)
    await state.set_state(AdForm.type)


@router.message(AdForm.type)
async def set_type(message: types.Message, state: FSMContext):
    """
    Обработка выбора типа: отправка или получение.
    """
    if message.text not in ["📤 Отправить", "📥 Получить"]:
        await message.answer("Пожалуйста, выберите один из вариантов кнопками.")
        return

    ad_type = "отправка" if message.text == "📤 Отправить" else "получение"
    await state.update_data(type=ad_type)

    await message.answer("Что вы хотите отправить?", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AdForm.description)


@router.message(AdForm.description)
async def input_description(message: types.Message, state: FSMContext):
    """
    Получает описание посылки от пользователя.
    """
    await state.update_data(description=message.text)
    await message.answer("Откуда будет отправка?\n\nПример: <code>Город, Страна</code>", parse_mode="HTML")
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
    await message.answer("Куда нужно доставить?\n\nПример: <code>Город, Страна</code>", parse_mode="HTML")
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
        "Введите дату в формате <code>ДД.ММ.ГГГГ</code>\n"
        "(максимум 30 дней вперёд)",
        parse_mode="HTML"
    )
    await state.set_state(AdForm.approx_date)


@router.message(AdForm.approx_date)
async def input_date(message: types.Message, state: FSMContext):
    """
    Получает дату в формате ДД.ММ.ГГГГ и проверяет её корректность.
    """
    ok, result = validate_date_input(message.text, max_days=30)
    if not ok:
        await message.answer(result, parse_mode="HTML")
        return

    await state.update_data(approx_date=result)
    await message.answer("💵 Укажите цену за доставку:")
    await state.set_state(AdForm.price)


@router.message(AdForm.price)
async def input_price(message: types.Message, state: FSMContext):
    """
    Финальный шаг. Получает цену, сохраняет объявление в БД.
    """
    await state.update_data(price=message.text)
    data = await state.get_data()
    telegram_id = message.from_user.id

    user = await get_user_or_reply(telegram_id, message)
    if not user:
        return

    async for session in get_session():
        new_ad = Ad(
            user_id=user.id,
            type=data["type"],
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

    await message.answer("✅ Объявление добавлено! Спасибо.")
    await state.clear()