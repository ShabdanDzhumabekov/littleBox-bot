from bot.testing.database import a_route, a_user, reset_database, save
from bot.testing.dispatcher import fake_bot, fresh_dispatcher
from bot.testing.fake_telegram import FakeTelegram
from bot.testing.telegram_updates import button_press_update

UNREGISTERED_USER_ID = 171


async def test_edit_route_button_from_unregistered_user_reports_route_not_found() -> None:
    await reset_database()
    route = a_route(a_user(telegram_id=170))
    await save(route)
    telegram = FakeTelegram()
    bot = fake_bot(telegram)
    dispatcher = fresh_dispatcher()

    await dispatcher.feed_update(bot, button_press_update(UNREGISTERED_USER_ID, f"edit_route_{route.id}"))

    assert telegram.callback_answers[-1].text == "❌ Маршрут не найден или не ваш"
