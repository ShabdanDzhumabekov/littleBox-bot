from datetime import date, timedelta

from bot.states import RouteForm
from bot.testing.database import a_user, an_ad, reset_database, save
from bot.testing.dispatcher import fake_bot, fresh_dispatcher, user_form
from bot.testing.fake_telegram import FakeTelegram
from bot.testing.telegram_updates import text_message_update

TRAVELER_ID = 90
SENDER_ID = 91
ANSWERS_BEFORE_CONDITIONS = {
    "from_city": "Бишкек",
    "from_country": "Кыргызстан",
    "to_city": "Белград",
    "to_country": "Сербия",
    "travel_date": date.today() + timedelta(days=7),
    "luggage": "до 2 кг",
}


async def test_route_form_finishes_when_matching_sender_blocked_bot() -> None:
    await reset_database()
    await save(a_user(telegram_id=TRAVELER_ID), an_ad(a_user(telegram_id=SENDER_ID)))
    telegram = FakeTelegram(blocked_chat_ids=frozenset({SENDER_ID}))
    bot = fake_bot(telegram)
    dispatcher = fresh_dispatcher()
    form = user_form(dispatcher, bot, TRAVELER_ID)
    await form.set_state(RouteForm.conditions)
    await form.set_data(ANSWERS_BEFORE_CONDITIONS)

    await dispatcher.feed_update(bot, text_message_update(TRAVELER_ID, "—"))

    assert await form.get_state() is None
