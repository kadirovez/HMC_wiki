
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.register import registration_crud
from src.models.auth.register_session import Registration
from src.schemas import RegistrationPasswordRequest, RegistrationUpdate
from src.schemas.base import StatusResponseSchema
from src.utils.password import get_password_hash


async def validate_password(
        db: AsyncSession,
        registration_session: Registration,
        obj_in: RegistrationPasswordRequest,
) -> StatusResponseSchema:
    ''' Checks password policy and stores password hash in database '''

    if not registration_session.email or not registration_session.username:
        raise HTTPException(
            status_code=401,
            detail='No user data'
        )

    # if not registration_session.email_is_confirmed:
    #     raise HTTPException(
    #         status_code=401,
    #         detail='Confirm your email first'
    #     )

    await registration_crud.reset(
        db=db,
        db_obj=registration_session,
        keep_fields={
            'username':True,
            'first_name':True,
            'last_name':True,
            'email':True,
            'email_is_confirmed':True,
            'email_code_sent':True,
            'email_code_id':True,
            'email_code_expire_at':True,
        }
    )

    await registration_crud.update(
        db=db,
        id=registration_session.id,
        obj_in=RegistrationUpdate(
            password=get_password_hash(obj_in.password)
        )
    )

    return StatusResponseSchema(status=True)

