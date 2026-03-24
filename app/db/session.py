from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import get_settings
from typing import AsyncGenerator

settings = get_settings()

engine = create_async_engine(
    settings.DATABASE_URL, 
    pool_size = 10,
    max_overflow = 20,
    echo=settings.DEBUG
)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session