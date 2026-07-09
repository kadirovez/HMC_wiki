
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.register import registration_crud
from src.models.auth.register_session import Registration
from src.schemas.auth.registration import RegistrationEmailOTPRequest, RegistrationUpdate
from src.schemas.base import StatusResponseSchema


async def confirm_email_otp(
        db: AsyncSession,
        registration_session: Registration,
        obj_in: RegistrationEmailOTPRequest,
) -> StatusResponseSchema:
    ''' Checks email otp code '''

    if not registration_session.email_code_sent:
        raise HTTPException(
            status_code=400,
            detail='Request OTP first'
        )

    expire_at = registration_session.email_code_expire_at
    if expire_at and expire_at.tzinfo is None:
        expire_at = expire_at.replace(tzinfo=timezone.utc)
    if expire_at and expire_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail='OTP expired'
        )

    if registration_session.email_code_sent != obj_in.email_otp:
        raise HTTPException(
            status_code=401,
            detail='Invalid OTP code'
        )

    await registration_crud.update(
        db=db,
        id=registration_session.id,
        obj_in=RegistrationUpdate(
            email_is_confirmed=True,
            email_code_sent=None,
            email_code_id=None,
            email_code_expire_at=None,
        ),
    )

    return StatusResponseSchema(status=True)

