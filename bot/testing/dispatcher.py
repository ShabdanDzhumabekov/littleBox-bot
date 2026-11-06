from functools import cache

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers import setup_routers
from bot.testing.fake_telegram import FakeTelegram


def fresh_dispatcher() -> Dispatcher:
    # Роутеры хендлеров живут на уровне модулей и подключаются только один раз,
    # поэтому тесты делят один диспетчер, а хранилище FSM у каждого теста своё.
    dispatcher = _dispatcher_with_bot_routers()
    dispatcher.fsm.storage = MemoryStorage()
    return dispatcher


def fake_bot(telegram: FakeTelegram) -> Bot:
    return Bot("42:TEST", session=telegram, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


def user_form(dispatcher: Dispatcher, bot: Bot, user_id: int) -> FSMContext:
    key = StorageKey(bot_id=bot.id, chat_id=user_id, user_id=user_id)
    return FSMContext(storage=dispatcher.storage, key=key)


@cache
def _dispatcher_with_bot_routers() -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher.include_router(setup_routers())
    return dispatcher
