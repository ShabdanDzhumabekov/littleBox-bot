"""
FSM: Подача объявления пользователем. Сохраняется в таблицу ads.
"""

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from bot.states.ads import AdForm
from bot.database.models import Ad, User
from bot.database.db import get_session
from sqlalchemy import select
from datetime import date

router = Router()


# 🔹 Старт — пользователь нажал кнопку "Разместить объявление"
@router.message(F.text == "📦 Разместить объявление")
async def choose_type(message: types.Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📤 Отправить"), KeyboardButton(text="📥 Получить")]
        ],
        resize_keyboard=True
    )
    await message.answer("Вы хотите отправить или получить посылку?", reply_markup=keyboard)
    await state.set_state(AdForm.type)


# 🔹 Шаг 1 — выбор типа: отправка или получение
@router.message(AdForm.type)
async def set_type(message: types.Message, state: FSMContext):
    if message.text not in ["📤 Отправить", "📥 Получить"]:
        await message.answer("Пожалуйста, выберите один из вариантов кнопками.")
        return

    ad_type = "отправка" if message.text == "📤 Отправить" else "получение"
    await state.update_data(type=ad_type)

    await message.answer("Что вы хотите отправить?", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AdForm.description)


# 🔹 Шаг 2 — описание посылки
@router.message(AdForm.description)
async def input_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Откуда будет отправка?")
    await state.set_state(AdForm.from_location)


# 🔹 Шаг 3 — откуда
@router.message(AdForm.from_location)
async def input_from_location(message: types.Message, state: FSMContext):
    await state.update_data(from_location=message.text)
    await message.answer("Куда нужно доставить?")
    await state.set_state(AdForm.to_location)


# 🔹 Шаг 4 — куда
@router.message(AdForm.to_location)
async def input_to_location(message: types.Message, state: FSMContext):
    await state.update_data(to_location=message.text)
    await message.answer("Примерная дата доставки (текстом)?")
    await state.set_state(AdForm.approx_date_text)


# 🔹 Шаг 5 — примерная дата
@router.message(AdForm.approx_date_text)
async def input_approx_date(message: types.Message, state: FSMContext):
    await state.update_data(approx_date_text=message.text)
    await message.answer("Укажите желаемую цену (в $ или сумме)")
    await state.set_state(AdForm.price)


# 🔹 Финальный шаг — цена + сохранение
@router.message(AdForm.price)
async def input_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()
    telegram_id = message.from_user.id

    async for session in get_session():
        # Получаем user.id по telegram_id
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            await message.answer("❗ Вы ещё не зарегистрированы. Введите /start.")
            return
        
        new_ad = Ad(
            user_id=user.id,
            type=data["type"],
            description=data["description"],
            from_location=data["from_location"],
            to_location=data["to_location"],
            approx_date_text=data["approx_date_text"],
            price=data["price"]
        )
        session.add(new_ad)
        await session.commit()

    await message.answer("✅ Объявление добавлено! Спасибо.")
    await state.clear()