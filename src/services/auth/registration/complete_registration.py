
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.register import registration_crud
from src.crud.auth.user import user_crud
from src.models.auth.register_session import Registration
from src.schemas import UserCreate
from src.schemas.auth.registration import RegistrationCompleteResponse, RegistrationUpdate


async def complete_registration(
        db: AsyncSession,
        registration_session: Registration,
) -> RegistrationCompleteResponse:
    if registration_session.is_completed:
        raise HTTPException(
            status_code=400,
            detail='Session already completed'
        )

    if not registration_session.password_is_confirmed:
        raise HTTPException(
            status_code=400,
            detail='Confirm password first'
        )

    user = await user_crud.create(
        db=db,
        obj_in=UserCreate(
            username=registration_session.username,
            first_name=registration_session.first_name,
            last_name=registration_session.last_name,
            password=registration_session.password,
            email=registration_session.email,
            email_is_confirmed=True,
            is_active=True,
        ),
    )

    await registration_crud.update(
        db=db,
        id=registration_session.id,
        obj_in=RegistrationUpdate(is_completed=True),
    )

    return RegistrationCompleteResponse(user_id=user.id)
