
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

from src.core.database import AsyncSessionLocal

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    '''
    Dependency for getting database session
    '''
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()