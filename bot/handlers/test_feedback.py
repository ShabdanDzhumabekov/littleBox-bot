from bot.config import ADMIN_ID
from bot.database.models import Feedback
from bot.testing.database import a_user, reset_database, save
from bot.testing.dispatcher import fake_bot, fresh_dispatcher
from bot.testing.fake_telegram import FakeTelegram
from bot.testing.telegram_updates import text_message_update


async def test_feedback_list_renders_html_in_feedback_as_plain_text() -> None:
    await reset_database()
    await save(Feedback(user=a_user(telegram_id=40), text="<b>спасибо</b>"))
    telegram = FakeTelegram()
    bot = fake_bot(telegram)
    dispatcher = fresh_dispatcher()

    await dispatcher.feed_update(bot, text_message_update(ADMIN_ID, "💬 Отзывы"))

    assert "&lt;b&gt;спасибо&lt;/b&gt;" in telegram.texts_sent_to(ADMIN_ID)[-1]
