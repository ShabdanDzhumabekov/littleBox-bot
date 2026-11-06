from datetime import date, timedelta

from bot.states import AdForm
from bot.testing.database import a_route, a_user, reset_database, save
from bot.testing.dispatcher import fake_bot, fresh_dispatcher, user_form
from bot.testing.fake_telegram import FakeTelegram
from bot.testing.telegram_updates import text_message_update

SENDER_ID = 80
TRAVELER_ID = 81
ANSWERS_BEFORE_PRICE = {
    "description": "Документы",
    "from_city": "Бишкек",
    "from_country": "Кыргызстан",
    "to_city": "Белград",
    "to_country": "Сербия",
    "approx_date": date.today() + timedelta(days=7),
}


async def test_ad_form_finishes_when_matching_traveler_blocked_bot() -> None:
    await reset_database()
    await save(a_user(telegram_id=SENDER_ID), a_route(a_user(telegram_id=TRAVELER_ID)))
    telegram = FakeTelegram(blocked_chat_ids=frozenset({TRAVELER_ID}))
    bot = fake_bot(telegram)
    dispatcher = fresh_dispatcher()
    form = user_form(dispatcher, bot, SENDER_ID)
    await form.set_state(AdForm.price)
    await form.set_data(ANSWERS_BEFORE_PRICE)

    await dispatcher.feed_update(bot, text_message_update(SENDER_ID, "10"))

    assert await form.get_state() is None
