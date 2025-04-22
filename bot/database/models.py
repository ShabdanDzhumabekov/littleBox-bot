"""
Модели базы данных: User, Ad, Route.
Используются SQLAlchemy ORM + асинхронное подключение.
"""

from sqlalchemy import Column, Integer, String, BigInteger, Text, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, date
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
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    type = Column(String, nullable=False)  # отправка / получение
    description = Column(String, nullable=False)

    from_city = Column(String, nullable=False)
    from_country = Column(String, nullable=False)
    to_city = Column(String, nullable=False)
    to_country = Column(String, nullable=False)

    approx_date = Column(Date, nullable=False)  # до какой даты актуально
    price = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)  # <-- дата публикации

    user = relationship("User", back_populates="ads")


# 🛫 Маршрут путешественника
class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    from_city = Column(String)
    from_country = Column(String)
    to_city = Column(String)
    to_country = Column(String)
    
    travel_date = Column(Date)
    luggage = Column(String)
    conditions = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="routes")