
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import settings
from src.crud.auth.login import login_crud
from src.models.auth.login_session import Login
from src.schemas import LoginUpdate
from src.schemas.base import StatusResponseSchema
from src.utils.email import send_email
from src.utils.generator import generate_otp


async def send_email_otp(
        db: AsyncSession,
        login_session: Login,
) -> StatusResponseSchema:

    # Check
    if not login_session.password_is_validated:
        raise HTTPException(
            status_code=400,
            detail='Validate password first'
        )

    if not login_session.email:
        raise HTTPException(
            status_code=400,
            detail='Email not found in session'
        )

    # Create otp code
    otp_code, otp_code_id, otp_expire_at = generate_otp(
        length=6,
        timeout=settings.email_code_timeout,
    )
    otp_code = otp_code[:6].zfill(6)

    # Action
    await send_email(otp_code)

    await login_crud.update(
        db=db,
        id=login_session.id,
        obj_in=LoginUpdate(
            email_code_sent=otp_code,
            email_code_id=otp_code_id,
            email_code_expire_at=otp_expire_at,
        )
    )

    return StatusResponseSchema(status=True)

