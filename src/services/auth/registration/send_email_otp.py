
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from src.core.settings import settings
from src.crud.auth.register import registration_crud
from src.models.auth.register_session import Registration
from src.schemas.auth.registration import RegistrationUpdate
from src.schemas.base import StatusResponseSchema
from src.utils.email import send_email
from src.utils.generator import generate_otp



async def send_email_otp(
        db: AsyncSession,
        registration_session: Registration,
) -> StatusResponseSchema:
    ''' Function for sending email otp code '''

    if not registration_session.email:
        raise HTTPException(
            status_code=400,
            detail='Submit email'
        )

    if registration_session.email_is_confirmed:
        raise HTTPException(
            status_code=400,
            detail='Email already confirmed'
        )

    otp_code, otp_code_id, otp_expire_at = generate_otp(
        length=6,
        timeout=settings.email_code_timeout,
    )
    otp_code = otp_code[:6].zfill(6)

    # in this case otp code will be printed in terminal
    await send_email(otp_code)

    await registration_crud.update(
        db=db,
        id=registration_session.id,
        obj_in=RegistrationUpdate(
            email_code_sent=otp_code,
            email_code_id=otp_code_id,
            email_code_expire_at=otp_expire_at,
        ),
    )

    return StatusResponseSchema(status=True)

