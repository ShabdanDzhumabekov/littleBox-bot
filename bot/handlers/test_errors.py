import pytest
from aiogram.fsm.state import State
from geopy.exc import GeocoderServiceError, GeocoderTimedOut, GeocoderUnavailable

from bot.states import AdForm, FindAdForm, FindRouteForm
from bot.testing.dispatcher import fake_bot, fresh_dispatcher, user_form
from bot.testing.fake_geocoder import geocoding_failure
from bot.testing.fake_telegram import FakeTelegram
from bot.testing.telegram_updates import text_message_update

USER_ID = 130


@pytest.mark.parametrize(
    ("form_state", "geocoder_error"),
    [
        (AdForm.from_location, GeocoderUnavailable("Service unavailable")),
        (FindAdForm.from_location, GeocoderTimedOut("Timed out")),
        (FindRouteForm.to_location, GeocoderUnavailable("Too many requests")),
    ],
    ids=["ad-form-unavailable", "ad-search-timeout", "route-search-unavailable"],
)
async def test_location_step_reports_temporary_geocoder_failure(
    form_state: State, geocoder_error: GeocoderServiceError
) -> None:
    telegram = FakeTelegram()
    bot = fake_bot(telegram)
    dispatcher = fresh_dispatcher()
    form = user_form(dispatcher, bot, USER_ID)
    await form.set_state(form_state)
    await form.set_data({"from_city": "Бишкек", "from_country": "Кыргызстан"})

    with geocoding_failure(geocoder_error):
        await dispatcher.feed_update(bot, text_message_update(USER_ID, "Белград, Сербия"))

    assert telegram.texts_sent_to(USER_ID) == ["🌐 Временная ошибка при определении города. Попробуйте ещё раз."]
