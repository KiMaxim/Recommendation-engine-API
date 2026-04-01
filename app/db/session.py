from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import get_settings
from typing import AsyncGenerator

settings = get_settings()

# Initialize async database engine with performance-tuned connection pool
# pool_size: minimum connections; max_overflow: extra connections under load
engine = create_async_engine(
    settings.DATABASE_URL, 
    pool_size=settings.POOL_SIZE,
    max_overflow=settings.MAX_OVERFLOW,
    echo=settings.DEBUG  # Logs SQL queries when DEBUG=True
)

# Configure session factory for creating AsyncSession instances
# expire_on_commit=False keeps loaded objects in memory after commit
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Dependency provider for FastAPI route handlers to access database sessions
# Automatically handles session lifecycle (create, commit, rollback, cleanup)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session