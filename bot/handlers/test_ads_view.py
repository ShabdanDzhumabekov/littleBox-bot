from bot.states import FindAdForm
from bot.testing.database import a_user, an_ad, reset_database, save
from bot.testing.dispatcher import fake_bot, fresh_dispatcher, user_form
from bot.testing.fake_geocoder import geocoding_of
from bot.testing.fake_telegram import FakeTelegram
from bot.testing.telegram_updates import text_message_update

SENDER_ID = 21


async def test_ad_search_renders_html_in_description_as_plain_text() -> None:
    await reset_database()
    await save(an_ad(a_user(telegram_id=20), description="<коробка>"))
    telegram = FakeTelegram()
    bot = fake_bot(telegram)
    dispatcher = fresh_dispatcher()
    form = user_form(dispatcher, bot, SENDER_ID)
    await form.set_state(FindAdForm.to_location)
    await form.set_data({"from_city": "Бишкек", "from_country": "Кыргызстан"})

    with geocoding_of({"Белград, Сербия": ("Белград", "Сербия")}):
        await dispatcher.feed_update(bot, text_message_update(SENDER_ID, "Белград, Сербия"))

    assert "📝 <i>&lt;коробка&gt;</i>" in telegram.texts_sent_to(SENDER_ID)[-1]
