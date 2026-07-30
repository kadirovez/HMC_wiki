
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.core.settings import settings


# Create async database engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
    pool_pre_ping=True
)


# Create session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

class Base(DeclarativeBase):
    pass

async def init_db() -> None :
    ''' Initialize database tables '''
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

async def close_db() -> None :
    ''' Close database connections'''
    await engine.dispose()


