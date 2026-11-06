import asyncio

import pytest


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    # Каждое открытое соединение aiosqlite держит поток без daemon, он не даст процессу завершиться.
    from bot.database.db import engine

    asyncio.run(engine.dispose())
