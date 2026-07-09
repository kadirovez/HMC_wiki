
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.register import registration_crud
from src.models.auth.register_session import Registration
from src.schemas.base import StatusResponseSchema


async def cancel_registration(
        db: AsyncSession,
        registration_session: Registration,
) -> StatusResponseSchema:
    ''' Deletes registration session '''

    result = await registration_crud.delete(
        db=db,
        id=registration_session.id,
    )
    if not result:
        raise HTTPException(
            status_code=401,
            detail='Something went wrong'
        )

    return StatusResponseSchema(status=True)

