
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.register import registration_crud
from src.models.auth.register_session import Registration
from src.schemas import RegistrationConfirmPasswordRequest, RegistrationUpdate
from src.schemas.base import StatusResponseSchema
from src.utils.password import verify_password


async def confirm_password(
        db: AsyncSession,
        registration_session: Registration,
        obj_in: RegistrationConfirmPasswordRequest,
) -> StatusResponseSchema:
    ''' Confirms existing password (double check) '''

    if not registration_session.password:
        raise HTTPException(
            status_code=404,
            detail='Create your password first'
        )

    await registration_crud.reset(
        db=db,
        db_obj=registration_session,
        keep_fields={
            'username':True,
            'first_name':True,
            'last_name':True,
            'password':True,
            'email':True,
            'email_is_confirmed':True,
            'email_code_sent':True,
            'email_code_id':True,
            'email_code_expire_at':True,
        }
    )

    if not verify_password(obj_in.confirm_password, registration_session.password):
        raise HTTPException(
            status_code=401,
            detail='Entered password did not match'
        )

    await registration_crud.update(
        db=db,
        id=registration_session.id,
        obj_in=RegistrationUpdate(
            password_is_confirmed=True
        )
    )

    return StatusResponseSchema(status=True)
