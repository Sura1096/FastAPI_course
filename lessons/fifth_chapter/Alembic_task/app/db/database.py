from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from ..core.config import settings


engine = create_async_engine(settings.ASYNC_DB_URL)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


class Base(DeclarativeBase):
    pass


async def get_async_session():
    async with async_session_maker() as session:
        yield session
