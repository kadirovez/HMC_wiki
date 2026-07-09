
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.login import login_crud
from src.models.auth.login_session import Login
from src.schemas import LoginEmailOTPRequest, LoginUpdate
from src.schemas.base import StatusResponseSchema


async def confirm_email_otp(
        db: AsyncSession,
        login_session: Login,
        obj_in: LoginEmailOTPRequest,
) -> StatusResponseSchema:

    if not login_session.email_code_sent:
        raise HTTPException(
            status_code=400,
            detail='Email OTP code was not sent'
        )

    expire_at = login_session.email_code_expire_at
    if expire_at and expire_at.tzinfo is None:
        expire_at = expire_at.replace(tzinfo=timezone.utc)
    if expire_at and expire_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=401,
            detail='OTP code expired'
        )

    if login_session.email_code_sent != obj_in.email_otp:
        raise HTTPException(
            status_code=401,
            detail='Wrong otp code'
        )

    await login_crud.update(
        db=db,
        id=login_session.id,
        obj_in=LoginUpdate(
            email_is_confirmed=True,
            email_code_sent=None,
            email_code_id=None,
            email_code_expire_at=None,
        )
    )

    return StatusResponseSchema(status=True)
