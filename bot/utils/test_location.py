import asyncio
import threading
from typing import Any
from unittest.mock import patch

from bot.states import AdForm
from bot.testing.dispatcher import fake_bot, fresh_dispatcher, user_form
from bot.testing.fake_telegram import FakeTelegram
from bot.testing.telegram_updates import text_message_update
from bot.utils import location

SENDER_ID = 140
OTHER_USER_ID = 141


class GeocoderWaitingForOtherUser:
    """Держит поиск города, пока бот не ответит другому пользователю, но не дольше секунды."""

    def __init__(self) -> None:
        self.lookup_started = threading.Event()
        self.other_user_answered = threading.Event()
        self.has_seen_other_user_answered = False

    def geocode(self, query: str, **options: Any) -> None:
        self.lookup_started.set()
        self.has_seen_other_user_answered = self.other_user_answered.wait(timeout=1)


async def test_city_lookup_does_not_stop_bot_from_answering_other_users() -> None:
    telegram = FakeTelegram()
    bot = fake_bot(telegram)
    dispatcher = fresh_dispatcher()
    await user_form(dispatcher, bot, SENDER_ID).set_state(AdForm.from_location)
    geocoder = GeocoderWaitingForOtherUser()

    async def other_user_asks_for_help_during_lookup() -> None:
        await asyncio.to_thread(geocoder.lookup_started.wait, 1)
        await dispatcher.feed_update(bot, text_message_update(OTHER_USER_ID, "/help"))
        geocoder.other_user_answered.set()

    with patch.object(location, "geolocator", geocoder):
        await asyncio.gather(
            dispatcher.feed_update(bot, text_message_update(SENDER_ID, "Бишкек, Кыргызстан")),
            other_user_asks_for_help_during_lookup(),
        )

    assert geocoder.has_seen_other_user_answered
