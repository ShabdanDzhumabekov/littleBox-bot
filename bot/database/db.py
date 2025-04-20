"""
Настройка подключения к PostgreSQL через SQLAlchemy (async).
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from bot.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

# Строка подключения к базе в формате для asyncpg
DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Создание движка подключения
engine = create_async_engine(DATABASE_URL, echo=True)

# Создание асинхронной сессии
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Базовый класс для моделей
class Base(DeclarativeBase):
    pass

# Функция для получения сессии (используется в хендлерах или бизнес-логике)
async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session