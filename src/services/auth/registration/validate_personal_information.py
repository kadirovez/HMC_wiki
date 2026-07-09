
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.register import registration_crud
from src.crud.auth.user import user_crud
from src.models.auth.register_session import Registration
from src.schemas.auth.registration import RegistrationProfileRequest, RegistrationUpdate
from src.schemas.base import StatusResponseSchema


async def validate_personal_information(
        db: AsyncSession,
        registration_session: Registration,
        obj_in: RegistrationProfileRequest,
) -> StatusResponseSchema:
    ''' Validates personal information : username, first name, last name, email '''

    if await user_crud.get_by_username(
            db=db,
            username=obj_in.username
    ):
        raise HTTPException(
            status_code=409,
            detail='username already taken'
        )

    if await user_crud.get_by_email(
            db=db,
            email=obj_in.email
    ):
        raise HTTPException(
            status_code=409,
            detail='Email already taken'
        )

    await registration_crud.reset(
        db=db,
        db_obj=registration_session,
        keep_fields={},
    )

    await registration_crud.update(
        db=db,
        id=registration_session.id,
        obj_in=RegistrationUpdate(
            first_name=obj_in.first_name.title(),
            last_name=obj_in.last_name.title(),
            username=obj_in.username,
            email=obj_in.email,
        ),
    )

    return StatusResponseSchema(status=True)

