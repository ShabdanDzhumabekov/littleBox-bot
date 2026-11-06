"""
Настройка подключения к PostgreSQL через SQLAlchemy (async).
"""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from bot.config import DATABASE_URL

# Создание движка подключения
engine = create_async_engine(DATABASE_URL)

# Создание асинхронной сессии
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# Базовый класс для моделей
class Base(DeclarativeBase):
    pass
