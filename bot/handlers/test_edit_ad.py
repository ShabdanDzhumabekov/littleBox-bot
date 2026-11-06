from bot.testing.database import a_user, an_ad, reset_database, save
from bot.testing.dispatcher import fake_bot, fresh_dispatcher
from bot.testing.fake_telegram import FakeTelegram
from bot.testing.telegram_updates import button_press_update

UNREGISTERED_USER_ID = 161


async def test_edit_ad_button_from_unregistered_user_reports_ad_not_found() -> None:
    await reset_database()
    ad = an_ad(a_user(telegram_id=160))
    await save(ad)
    telegram = FakeTelegram()
    bot = fake_bot(telegram)
    dispatcher = fresh_dispatcher()

    await dispatcher.feed_update(bot, button_press_update(UNREGISTERED_USER_ID, f"edit_ad_{ad.id}"))

    assert telegram.callback_answers[-1].text == "❌ Объявление не найдено или не ваше"
