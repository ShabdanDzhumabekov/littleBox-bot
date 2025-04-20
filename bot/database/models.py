"""
Модели базы данных: User, Ad, Route.
Используются SQLAlchemy ORM + асинхронное подключение.
"""

from sqlalchemy import Column, Integer, String, BigInteger, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from bot.database.db import Base

# 👤 Пользователь Telegram
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String)
    created_at = Column(Date)

    ads = relationship("Ad", back_populates="user", cascade="all, delete-orphan")
    routes = relationship("Route", back_populates="user", cascade="all, delete-orphan")


# 📦 Объявление о передаче посылки
class Ad(Base):
    __tablename__ = "ads"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String)  # 'отправка' или 'получение'
    description = Column(Text)
    from_location = Column(String)
    to_location = Column(String)
    approx_date_text = Column(String)  # 👉 Текстовое поле вместо даты
    price = Column(String)

    user = relationship("User", back_populates="ads")


# 🛫 Маршрут путешественника
class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    from_location = Column(String)
    to_location = Column(String)
    travel_date = Column(Date)
    luggage = Column(String)
    conditions = Column(String)

    user = relationship("User", back_populates="routes")