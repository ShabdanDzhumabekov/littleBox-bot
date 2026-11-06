import pytest
from aiogram.fsm.state import State

from bot.handlers.feedback import FeedbackForm
from bot.states import AdForm, FindAdForm, FindRouteForm, RouteForm
from bot.testing.dispatcher import fake_bot, fresh_dispatcher, user_form
from bot.testing.fake_geocoder import geocoding_of
from bot.testing.fake_telegram import FakeTelegram
from bot.testing.telegram_updates import text_message_update

USER_ID = 50


@pytest.mark.parametrize(
    ("form_state", "button", "expected_state"),
    [
        (AdForm.description, "🔍 Найти путешественника", FindRouteForm.from_location),
        (AdForm.price, "🛫 Я лечу (маршрут)", RouteForm.from_location),
        (RouteForm.luggage, "🔍 Найти посылку", FindAdForm.from_location),
        (FindRouteForm.from_location, "💬 Оставить отзыв", FeedbackForm.writing),
    ],
    ids=["ad-description", "ad-price", "route-luggage", "route-search"],
)
async def test_menu_button_pressed_during_form_starts_its_own_flow(
    form_state: State, button: str, expected_state: State
) -> None:
    telegram = FakeTelegram()
    bot = fake_bot(telegram)
    dispatcher = fresh_dispatcher()
    form = user_form(dispatcher, bot, USER_ID)
    await form.set_state(form_state)

    with geocoding_of({}):
        await dispatcher.feed_update(bot, text_message_update(USER_ID, button))

    assert await form.get_state() == expected_state.state
