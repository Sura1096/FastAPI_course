from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from ..core.config import settings


engine = create_async_engine(settings.ASYNC_DATABASE_URL)  # создали движок БД
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)  # передали движок в создатель сессий


# Метатаблица, которая позволит создавать модели SQLAlchemy
class Base(DeclarativeBase):
    pass


async def get_async_session():
    async with async_session_maker() as session:
        yield session
