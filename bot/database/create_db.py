"""
Скрипт для создания всех таблиц в базе данных PostgreSQL.
Вызывается один раз при инициализации проекта или при сбросе схемы (если не используется Alembic).
"""

import asyncio
from bot.database.db import engine, Base
from bot.database import models

async def create_all():
    """
    Создаёт все таблицы, описанные в моделях SQLAlchemy.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create_all())