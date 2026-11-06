"""
Кнопка «Связаться с автором» под объявлением или маршрутом автора без username.
Бот отправляет автору username того, кто нажал кнопку, и автор пишет первым.
"""

from aiogram import Router, types
from aiogram.exceptions import TelegramForbiddenError
from sqlalchemy.orm import selectinload

from bot.database.db import SessionLocal
from bot.database.models import Ad, Route, User
from bot.utils import format_ad, format_route

router = Router()


@router.callback_query(lambda c: c.data.startswith("contact_ad_"))
async def contact_ad_author(callback: types.CallbackQuery):
    ad_id = int(callback.data.split("_")[-1])

    async with SessionLocal() as session:
        ad = await session.get(Ad, ad_id, options=[selectinload(Ad.user)])

    if not ad:
        await callback.answer("❌ Объявление уже удалено", show_alert=True)
        return

    await _pass_username_to_author(callback, ad.user, "по объявлению:\n\n" + format_ad(ad))


@router.callback_query(lambda c: c.data.startswith("contact_route_"))
async def contact_route_author(callback: types.CallbackQuery):
    route_id = int(callback.data.split("_")[-1])

    async with SessionLocal() as session:
        route = await session.get(Route, route_id, options=[selectinload(Route.user)])

    if not route:
        await callback.answer("❌ Маршрут уже удалён", show_alert=True)
        return

    await _pass_username_to_author(callback, route.user, "по маршруту:\n\n" + format_route(route))


async def _pass_username_to_author(callback: types.CallbackQuery, author: User, listing_text: str) -> None:
    if not callback.from_user.username:
        await callback.answer("Чтобы автор смог вам написать, укажите username в настройках Telegram.", show_alert=True)
        return

    try:
        await callback.bot.send_message(
            author.telegram_id,
            f"👋 @{callback.from_user.username} хочет связаться с вами {listing_text}",
            parse_mode="HTML"
        )
    except TelegramForbiddenError:
        await callback.answer("😔 Автор больше не пользуется ботом", show_alert=True)
        return

    await callback.answer("✅ Автор получил ваш username и сможет вам написать.", show_alert=True)
