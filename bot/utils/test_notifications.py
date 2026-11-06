from bot.testing.database import a_route, a_user, an_ad, reset_database, save
from bot.testing.dispatcher import fake_bot
from bot.testing.fake_telegram import FakeTelegram
from bot.utils.notifications import notify_about_new_ad


async def test_new_ad_still_reaches_travelers_after_one_blocked_bot() -> None:
    await reset_database()
    ad = an_ad(a_user(telegram_id=100))
    await save(ad, a_route(a_user(telegram_id=101)), a_route(a_user(telegram_id=102)))
    telegram = FakeTelegram(blocked_chat_ids=frozenset({101}))

    await notify_about_new_ad(fake_bot(telegram), ad.id)

    assert len(telegram.texts_sent_to(102)) == 1
