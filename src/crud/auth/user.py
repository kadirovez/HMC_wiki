
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.base import CRUDBase
from src.models.auth.user import User
from src.schemas.auth.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    ''' CRUD for user records '''

    async def get_by_username(
            self,
            db: AsyncSession,
            username: str,
    ) -> Optional[User]:
        result = await db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def get_by_email(
            self,
            db: AsyncSession,
            email: str,
    ) -> Optional[User]:
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def create(
            self,
            db: AsyncSession,
            obj_in: UserCreate,
    ) -> User:
        data = obj_in.model_dump()
        email_is_confirmed = data.pop('email_is_confirmed', False)
        data['email_confirmed'] = email_is_confirmed
        user = User(**data)
        await self._check_unique_fields(db=db, data=data)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def disable(
            self,
            db: AsyncSession,
            db_obj: User
    ) -> User:
        db_obj.is_active = False
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def enable(
            self,
            db: AsyncSession,
            db_obj: User
    ) -> User:
        db_obj.is_active = True
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


user_crud = CRUDUser(User)
