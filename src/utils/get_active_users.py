
from sqlalchemy.sql import select
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.auth.user import User


async def get_active_users(db: AsyncSession):

    # it doesnt get new sessions, instead it shows total amount of users
    result = await db.execute(
        select(func.count()).select_from(User)
    )

    users_count = result.scalar_one()
    return users_count
