from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.config import settings



engine = create_async_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = async_sessionmaker[AsyncSession](
    bind=engine,
    expire_on_commit=False,
    autoflush=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as db:
        yield db