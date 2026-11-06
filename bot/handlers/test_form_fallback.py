import pytest
from aiogram.fsm.state import State

from bot.states import AdForm, RouteForm
from bot.testing.dispatcher import fake_bot, fresh_dispatcher, user_form
from bot.testing.fake_telegram import FakeTelegram
from bot.testing.telegram_updates import sticker_message_update

USER_ID = 60

FORM_STEPS = pytest.mark.parametrize(
    "form_state",
    [AdForm.description, AdForm.approx_date, RouteForm.from_location],
    ids=["text-step", "date-step", "location-step"],
)


@FORM_STEPS
async def test_sticker_during_form_asks_for_text_answer(form_state: State) -> None:
    telegram = FakeTelegram()
    bot = fake_bot(telegram)
    dispatcher = fresh_dispatcher()
    await user_form(dispatcher, bot, USER_ID).set_state(form_state)

    await dispatcher.feed_update(bot, sticker_message_update(USER_ID))

    assert telegram.texts_sent_to(USER_ID) == ["✍️ Пожалуйста, отправьте ответ текстом."]


@FORM_STEPS
async def test_sticker_during_form_keeps_current_step(form_state: State) -> None:
    telegram = FakeTelegram()
    bot = fake_bot(telegram)
    dispatcher = fresh_dispatcher()
    form = user_form(dispatcher, bot, USER_ID)
    await form.set_state(form_state)

    await dispatcher.feed_update(bot, sticker_message_update(USER_ID))

    assert await form.get_state() == form_state.state
