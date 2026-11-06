from bot.states import AdForm
from bot.testing.database import a_user, reset_database, save
from bot.testing.dispatcher import fake_bot, fresh_dispatcher, user_form
from bot.testing.fake_telegram import FakeTelegram
from bot.testing.telegram_updates import text_message_update

USER_ID = 70


async def test_my_ads_button_leaves_unfinished_form() -> None:
    await reset_database()
    await save(a_user(telegram_id=USER_ID))
    telegram = FakeTelegram()
    bot = fake_bot(telegram)
    dispatcher = fresh_dispatcher()
    form = user_form(dispatcher, bot, USER_ID)
    await form.set_state(AdForm.description)

    await dispatcher.feed_update(bot, text_message_update(USER_ID, "📋 Мои объявления"))

    assert await form.get_state() is None
