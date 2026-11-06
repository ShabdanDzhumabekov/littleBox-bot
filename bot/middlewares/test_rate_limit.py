from aiogram import Dispatcher, Router
from aiogram.types import CallbackQuery, Message

from bot.middlewares import RateLimitMiddleware
from bot.testing.dispatcher import fake_bot
from bot.testing.fake_telegram import FakeTelegram
from bot.testing.telegram_updates import button_press_update, text_message_update

USER_ID = 180


async def accept_message(message: Message) -> None:
    pass


async def confirm_button_press(callback: CallbackQuery) -> None:
    await callback.answer("button handled")


async def test_button_press_right_after_message_is_not_throttled() -> None:
    telegram = FakeTelegram()
    bot = fake_bot(telegram)
    router = Router()
    router.message.register(accept_message)
    router.callback_query.register(confirm_button_press)
    dispatcher = Dispatcher()
    dispatcher.message.middleware(RateLimitMiddleware(limit_seconds=0.8))
    dispatcher.callback_query.middleware(RateLimitMiddleware(limit_seconds=0.5))
    dispatcher.include_router(router)

    await dispatcher.feed_update(bot, text_message_update(USER_ID, "привет"))
    await dispatcher.feed_update(bot, button_press_update(USER_ID, "any"))

    assert telegram.callback_answers[-1].text == "button handled"
