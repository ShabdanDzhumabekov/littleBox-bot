from collections.abc import Callable

import pytest

from bot.database.models import Ad, Route, User
from bot.testing.database import a_route, a_user, an_ad, reset_database, save
from bot.testing.dispatcher import fake_bot, fresh_dispatcher
from bot.testing.fake_telegram import FakeTelegram
from bot.testing.telegram_updates import button_press_update

AUTHOR_ID = 210
VIEWER_ID = 211


async def viewer_presses(telegram: FakeTelegram, button: str, viewer_username: str | None) -> None:
    update = button_press_update(VIEWER_ID, button, username=viewer_username)
    await fresh_dispatcher().feed_update(fake_bot(telegram), update)


def answers_shown_to_viewer(telegram: FakeTelegram) -> list[str | None]:
    return [answer.text for answer in telegram.callback_answers]


@pytest.mark.parametrize(
    ("listing_of", "button_prefix", "first_line"),
    [
        (an_ad, "contact_ad_", "👋 @viewer хочет связаться с вами по объявлению:"),
        (a_route, "contact_route_", "👋 @viewer хочет связаться с вами по маршруту:"),
    ],
    ids=["ad", "route"],
)
async def test_contact_button_sends_viewer_username_to_author(
    listing_of: Callable[[User], Ad | Route], button_prefix: str, first_line: str
) -> None:
    await reset_database()
    listing = listing_of(a_user(telegram_id=AUTHOR_ID, username=None))
    await save(listing)
    telegram = FakeTelegram()

    await viewer_presses(telegram, f"{button_prefix}{listing.id}", viewer_username="viewer")

    assert [text.splitlines()[0] for text in telegram.texts_sent_to(AUTHOR_ID)] == [first_line]


async def test_contact_button_confirms_to_viewer_that_author_got_username() -> None:
    await reset_database()
    ad = an_ad(a_user(telegram_id=AUTHOR_ID, username=None))
    await save(ad)
    telegram = FakeTelegram()

    await viewer_presses(telegram, f"contact_ad_{ad.id}", viewer_username="viewer")

    assert answers_shown_to_viewer(telegram) == ["✅ Автор получил ваш username и сможет вам написать."]


async def test_contact_button_asks_viewer_without_username_to_set_one() -> None:
    await reset_database()
    ad = an_ad(a_user(telegram_id=AUTHOR_ID, username=None))
    await save(ad)
    telegram = FakeTelegram()

    await viewer_presses(telegram, f"contact_ad_{ad.id}", viewer_username=None)

    assert answers_shown_to_viewer(telegram) == ["Чтобы автор смог вам написать, укажите username в настройках Telegram."]


@pytest.mark.parametrize(
    ("button", "answer_text"),
    [("contact_ad_999", "❌ Объявление уже удалено"), ("contact_route_999", "❌ Маршрут уже удалён")],
    ids=["ad", "route"],
)
async def test_contact_button_under_deleted_listing_reports_it_is_gone(button: str, answer_text: str) -> None:
    await reset_database()
    telegram = FakeTelegram()

    await viewer_presses(telegram, button, viewer_username="viewer")

    assert answers_shown_to_viewer(telegram) == [answer_text]


async def test_contact_button_reports_author_who_blocked_bot() -> None:
    await reset_database()
    ad = an_ad(a_user(telegram_id=AUTHOR_ID, username=None))
    await save(ad)
    telegram = FakeTelegram(blocked_chat_ids=frozenset({AUTHOR_ID}))

    await viewer_presses(telegram, f"contact_ad_{ad.id}", viewer_username="viewer")

    assert answers_shown_to_viewer(telegram) == ["😔 Автор больше не пользуется ботом"]
