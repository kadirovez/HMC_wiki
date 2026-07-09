
from typing import Optional, List, Dict
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import settings
from src.crud.base import CRUDBase
from src.core.database import Base
from pydantic import BaseModel
from typing import TypeVar

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDSessionBase(CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base CRUD class for session models."""

    reset_values: dict = {}

    async def get_by_session(
            self,
            db: AsyncSession,
            session: str,
    ) -> Optional[ModelType]:
        """Get session row by session token."""
        db_obj = select(self.model).where(self.model.session == session)
        result = await db.execute(db_obj)
        return result.scalar_one_or_none()


    async def get_by_ip(
            self,
            db: AsyncSession,
            ip_address: str
    ) -> List[ModelType]:
        ''' Gets records by IP '''
        result = await db.execute(
            select(self.model)
            .where(self.model.ip_address == ip_address)
            .order_by(self.model.created_at.desc())
        )
        return list(result.scalars().all())

    def count_recent_by_ip(self):
        # Coming soon...
        pass


    async def reset(
            self,
            db: AsyncSession,
            db_obj: ModelType,
            keep_fields : Dict[str, bool] | None
    ) -> ModelType:
        ''' Reset session fields, while keeping specified ones '''
        if keep_fields is None:
            keep_fields =  {}

        # Reset values must be determined in inherited class
        reset_data = {}
        for field, reset_value in self.reset_values.items():
            if not keep_fields.get(field, False):
                reset_data[field] = reset_value

        for field, value in reset_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj


    async def cleanup(
            self,
            db: AsyncSession,
            expire_minute: int | None = None
    ) -> int:
        if expire_minute is None:
            expire_minute = settings.session_expire_minute

        cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=expire_minute)

        result = await db.execute(
            delete(self.model)
            .where(self.model.created_at < cutoff_time)
        )

        await db.commit()

        return result.rowcount

