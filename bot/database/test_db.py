import logging

import pytest

from bot.testing.database import a_user, an_ad, reset_database, save


async def test_saving_ad_keeps_its_text_out_of_logs(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO)
    await reset_database()

    await save(an_ad(a_user(telegram_id=150), description="Паспорт на имя Анны"))

    assert "Паспорт на имя Анны" not in caplog.text
