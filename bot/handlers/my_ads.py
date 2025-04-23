"""
📋 my_ads.py — Хендлеры для работы с личными объявлениями пользователя

Функции:
- Показывает все объявления и маршруты текущего пользователя
- Добавляет inline-кнопки ✏️ Редактировать и ❌ Удалить
- Обрабатывает callback-запросы на удаление объявлений и маршрутов

Используется только внутри меню "📋 Мои объявления"
"""

from aiogram import Router, types, F
from aiogram.types import CallbackQuery
from sqlalchemy import select
from bot.database.db import get_session
from bot.database.models import User, Ad, Route
from bot.utils import format_ad, format_route
from bot.keyboards.inline import ad_inline_keyboard, route_inline_keyboard

router = Router()

@router.message(F.text == "📋 Мои объявления")
async def my_ads(message: types.Message):
    """
    Обрабатывает команду "📋 Мои объявления"
    Показывает объявления (Ad) и маршруты (Route), созданные текущим пользователем
    """
    telegram_id = message.from_user.id

    async for session in get_session():
        stmt_user = select(User).where(User.telegram_id == telegram_id)
        result_user = await session.execute(stmt_user)
        user = result_user.scalar_one_or_none()

        if not user:
            await message.answer("❗ Вы ещё не зарегистрированы. Введите /start.")
            return

        # 📦 Получаем объявления
        stmt_ads = select(Ad).where(Ad.user_id == user.id).order_by(Ad.id.desc())
        result_ads = await session.execute(stmt_ads)
        ads = result_ads.scalars().all()

        if ads:
            await message.answer("📦 <b>Ваши объявления о посылках:</b>", parse_mode="HTML")
            for ad in ads:
                await message.answer(format_ad(ad), reply_markup=ad_inline_keyboard(ad.id), parse_mode="HTML")

        # 🛫 Получаем маршруты
        stmt_routes = select(Route).where(Route.user_id == user.id).order_by(Route.id.desc())
        result_routes = await session.execute(stmt_routes)
        routes = result_routes.scalars().all()

        if routes:
            await message.answer("🛫 <b>Ваши маршруты:</b>", parse_mode="HTML")
            for route in routes:
                await message.answer(format_route(route), reply_markup=route_inline_keyboard(route.id), parse_mode="HTML")

        if not ads and not routes:
            await message.answer("📭 У вас пока нет объявлений или маршрутов.")

@router.callback_query(lambda c: c.data.startswith("delete_ad_"))
async def delete_ad_callback(callback: CallbackQuery):
    """
    Удаляет объявление (Ad), если оно принадлежит текущему пользователю
    """
    telegram_id = callback.from_user.id
    ad_id = int(callback.data.split("_")[-1])

    async for session in get_session():
        stmt_user = select(User).where(User.telegram_id == telegram_id)
        result_user = await session.execute(stmt_user)
        user = result_user.scalar_one_or_none()

        if not user:
            await callback.message.answer("❗ Вы не зарегистрированы. Нажмите /start.")
            return

        stmt_ad = select(Ad).where(Ad.id == ad_id, Ad.user_id == user.id)
        result_ad = await session.execute(stmt_ad)
        ad = result_ad.scalar_one_or_none()

        if not ad:
            await callback.answer("⛔ Это объявление не найдено или не ваше.", show_alert=True)
            return

        await session.delete(ad)
        await session.commit()

        await callback.answer("✅ Объявление удалено!", show_alert=True)
        await callback.message.delete()

@router.callback_query(lambda c: c.data.startswith("delete_route_"))
async def delete_route_callback(callback: CallbackQuery):
    """
    Удаляет маршрут (Route), если он принадлежит текущему пользователю
    """
    telegram_id = callback.from_user.id
    route_id = int(callback.data.split("_")[-1])

    async for session in get_session():
        stmt_user = select(User).where(User.telegram_id == telegram_id)
        result_user = await session.execute(stmt_user)
        user = result_user.scalar_one_or_none()

        if not user:
            await callback.message.answer("❗ Вы не зарегистрированы. Введите /start.")
            return

        stmt_route = select(Route).where(Route.id == route_id, Route.user_id == user.id)
        result_route = await session.execute(stmt_route)
        route = result_route.scalar_one_or_none()

        if not route:
            await callback.answer("⛔ Этот маршрут не найден или не ваш.", show_alert=True)
            return

        await session.delete(route)
        await session.commit()

        await callback.answer("✅ Маршрут удалён!", show_alert=True)
        await callback.message.delete()