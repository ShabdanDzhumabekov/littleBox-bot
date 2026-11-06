from datetime import date, timedelta

from bot.testing.database import a_route, a_user, an_ad, reset_database, save
from bot.testing.dispatcher import fake_bot
from bot.testing.fake_telegram import FakeTelegram
from bot.utils.notifications import notify_about_new_ad, notify_about_new_route

YESTERDAY = date.today() - timedelta(days=1)


async def test_new_ad_still_reaches_travelers_after_one_blocked_bot() -> None:
    await reset_database()
    ad = an_ad(a_user(telegram_id=100))
    await save(ad, a_route(a_user(telegram_id=101)), a_route(a_user(telegram_id=102)))
    telegram = FakeTelegram(blocked_chat_ids=frozenset({101}))

    await notify_about_new_ad(fake_bot(telegram), ad.id)

    assert len(telegram.texts_sent_to(102)) == 1


async def test_new_ad_skips_traveler_whose_trip_is_over() -> None:
    await reset_database()
    ad = an_ad(a_user(telegram_id=110))
    await save(ad, a_route(a_user(telegram_id=111), travel_date=YESTERDAY))
    telegram = FakeTelegram()

    await notify_about_new_ad(fake_bot(telegram), ad.id)

    assert telegram.texts_sent_to(111) == []


async def test_new_route_skips_sender_whose_ad_expired() -> None:
    await reset_database()
    route = a_route(a_user(telegram_id=120))
    await save(route, an_ad(a_user(telegram_id=121), approx_date=YESTERDAY))
    telegram = FakeTelegram()

    await notify_about_new_route(fake_bot(telegram), route.id)

    assert telegram.texts_sent_to(121) == []
