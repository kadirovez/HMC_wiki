
from typing import Generic, TypeVar, Type, Optional

from fastapi import HTTPException
from sqlalchemy import select, inspect
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy import Boolean as SABoolean

from src.core.database import Base

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)

def _coerce_value(value: str, col_type):

    if value is None or value == '':
        return None
    if isinstance(col_type, SABoolean):
        return value.lower() in ('true', '1', 'yes')
    return value


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    ''' Base CRUD operations for all models '''

    def __init__(self, model: Type[ModelType], load_options : list | None = None):
        self.model = model
        self.load_options = load_options or []

        self._unique_fields = [
            col.name
            for col in inspect(model).columns
            if col.unique and col.name != 'id'
        ]

    def _apply_load_options(self, query):
        ''' Super puper tema which is nice to have, but not necessary to use '''
        for options in self.load_options:
            query = query.options(options)
        return query

    async def _check_unique_fields(
            self,
            db: AsyncSession,
            data: dict,
            exclude_id : int | None = None
    ):
        ''' Checks unique fields, raises 409 if violated '''
        for field in self._unique_fields:
            if field not in data or data[field] is None:
                continue

            query = select(self.model).where(
                getattr(self.model, field) == data[field]
            )

            if exclude_id:
                query = query.where(self.model.id != exclude_id)

            result = await db.execute(query)
            existing = result.scalar_one_or_none()

            if existing:
                raise HTTPException(
                    status_code=401,
                    detail='Field already exists'
                )

    async def get(
            self,
            db: AsyncSession,
            id: int
    ) -> Optional[ModelType]:
        ''' Gets record from database by ID '''
        query = select(self.model).where(self.model.id == id)
        query = self._apply_load_options(query)
        result = await db.execute(query)
        db_obj = result.scalar_one_or_none()

        if not db_obj:
            raise HTTPException(
                status_code=404,
                detail='Model not found'
            )
        return db_obj

    async def create(
            self,
            db: AsyncSession,
            obj_in: CreateSchemaType,
    ) -> ModelType:
        ''' Creates new record in database '''
        obj_in_data = obj_in.model_dump()
        await self._check_unique_fields(db=db, data=obj_in_data)

        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db: AsyncSession,
            id: int,
            obj_in: UpdateSchemaType
    ) -> ModelType:
        ''' Updates existing record '''
        db_obj = await self.get(db=db, id=id)
        obj_data = obj_in.model_dump(exclude_unset=True)
        await self._check_unique_fields(db=db, data=obj_data, exclude_id=db_obj.id)

        for key, value in obj_data.items():
            setattr(db_obj, key, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj


    async def delete(
            self,
            db: AsyncSession,
            id: int
    ) -> Optional[ModelType]:
        ''' Deletes record from database by ID '''
        db_obj = await self.get(db=db, id=id)
        await db.delete(db_obj)
        await db.commit()
        return db_obj

