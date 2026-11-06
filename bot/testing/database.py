from datetime import date, timedelta

from bot.database.db import Base, SessionLocal, engine
from bot.database.models import Ad, Route, User


async def reset_database() -> None:
    # Соединения в пуле привязаны к циклу событий предыдущего теста, их нельзя переиспользовать.
    await engine.dispose()
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


async def save(*rows: Base) -> None:
    async with SessionLocal() as session:
        session.add_all(rows)
        await session.commit()


def a_user(telegram_id: int, username: str | None = "traveler") -> User:
    return User(telegram_id=telegram_id, username=username, created_at=date.today())


def an_ad(user: User, description: str = "Документы", approx_date: date | None = None) -> Ad:
    return Ad(
        user=user,
        description=description,
        from_city="Бишкек",
        from_country="Кыргызстан",
        to_city="Белград",
        to_country="Сербия",
        approx_date=approx_date or date.today() + timedelta(days=7),
        price="10",
    )


def a_route(user: User, luggage: str = "до 2 кг", travel_date: date | None = None) -> Route:
    return Route(
        user=user,
        from_city="Бишкек",
        from_country="Кыргызстан",
        to_city="Белград",
        to_country="Сербия",
        travel_date=travel_date or date.today() + timedelta(days=7),
        luggage=luggage,
        conditions="—",
    )
