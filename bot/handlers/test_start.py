from bot.testing.database import reset_database
from bot.testing.dispatcher import fake_bot, fresh_dispatcher
from bot.testing.fake_telegram import FakeTelegram
from bot.testing.telegram_updates import text_message_update

USER_ID = 220


async def test_start_tells_new_user_without_username_how_contact_works() -> None:
    await reset_database()
    telegram = FakeTelegram()
    bot = fake_bot(telegram)
    dispatcher = fresh_dispatcher()

    await dispatcher.feed_update(bot, text_message_update(USER_ID, "/start"))

    assert telegram.texts_sent_to(USER_ID)[0].startswith("⚠️ У тебя скрыт username в Telegram.")
