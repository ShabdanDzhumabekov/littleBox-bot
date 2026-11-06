from bot.states import FindRouteForm
from bot.testing.database import a_route, a_user, reset_database, save
from bot.testing.dispatcher import fake_bot, fresh_dispatcher, user_form
from bot.testing.fake_geocoder import geocoding_of
from bot.testing.fake_telegram import FakeTelegram
from bot.testing.telegram_updates import text_message_update

SENDER_ID = 31
TRAVELER_ID = 32


async def search_routes_from_bishkek_to_belgrade(telegram: FakeTelegram) -> None:
    bot = fake_bot(telegram)
    dispatcher = fresh_dispatcher()
    form = user_form(dispatcher, bot, SENDER_ID)
    await form.set_state(FindRouteForm.to_location)
    await form.set_data({"from_city": "Бишкек", "from_country": "Кыргызстан"})

    with geocoding_of({"Белград, Сербия": ("Белград", "Сербия")}):
        await dispatcher.feed_update(bot, text_message_update(SENDER_ID, "Белград, Сербия"))


async def test_route_search_renders_html_in_luggage_as_plain_text() -> None:
    await reset_database()
    await save(a_route(a_user(telegram_id=TRAVELER_ID), luggage="<2 кг>"))
    telegram = FakeTelegram()

    await search_routes_from_bishkek_to_belgrade(telegram)

    assert "🧳 &lt;2 кг&gt;" in telegram.texts_sent_to(SENDER_ID)[-1]


async def test_route_search_offers_contact_button_when_traveler_has_no_username() -> None:
    await reset_database()
    route = a_route(a_user(telegram_id=TRAVELER_ID, username=None))
    await save(route)
    telegram = FakeTelegram()

    await search_routes_from_bishkek_to_belgrade(telegram)

    assert telegram.buttons_of_last_message_to(SENDER_ID) == [f"contact_route_{route.id}"]
