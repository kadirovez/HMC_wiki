
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.register import registration_crud
from src.deps.database import get_db
from src.deps.session import get_registration_session
from src.models.auth.register_session import Registration
from src.schemas.addons import Token
from src.schemas.auth.base import CreateSessionSchema
from src.schemas.auth.registration import (
    RegistrationProfileRequest,
    RegistrationPasswordRequest,
    RegistrationConfirmPasswordRequest,
    RegistrationCompleteResponse,
)
from src.schemas.base import StatusResponseSchema
from src.services.auth.registration import registration_service
from src.services.session import session_service
from src.utils.ip_address import get_ip

router = APIRouter(prefix='/registration', tags=['registration'])


@router.get('/start', response_model=Token)
async def start_registration(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    ''' Starts registration session '''
    ip_address = get_ip(request)
    return await session_service.start_session(
        db=db,
        ip_address=ip_address,
        crud=registration_crud,
        create_schema=CreateSessionSchema,
    )


@router.post('/personal-data', response_model=StatusResponseSchema)
async def submit_profile(
    obj_in: RegistrationProfileRequest,
    registration_session: Registration = Depends(get_registration_session),
    db: AsyncSession = Depends(get_db),
):
    '''
    Validating personal data:
    username, first name, last name, email
    '''
    return await registration_service.validate_personal_information(
        db=db,
        registration_session=registration_session,
        obj_in=obj_in,
    )


@router.post('/password', response_model=StatusResponseSchema)
async def submit_password(
    obj_in: RegistrationPasswordRequest,
    registration_session: Registration = Depends(get_registration_session),
    db: AsyncSession = Depends(get_db),
):
    ''' Validates password policy '''
    return await registration_service.validate_password(
        db=db,
        registration_session=registration_session,
        obj_in=obj_in,
    )


@router.post('/confirm-password', response_model=StatusResponseSchema)
async def confirm_password(
    obj_in: RegistrationConfirmPasswordRequest,
    registration_session: Registration = Depends(get_registration_session),
    db: AsyncSession = Depends(get_db),
):
    ''' Confirms password (double check) '''
    return await registration_service.confirm_password(
        db=db,
        registration_session=registration_session,
        obj_in=obj_in,
    )


@router.post('/complete-registration', response_model=RegistrationCompleteResponse)
async def complete_registration(
    registration_session: Registration = Depends(get_registration_session),
    db: AsyncSession = Depends(get_db),
):
    ''' Completes registration session and creates user by entered data '''
    return await registration_service.complete_registration(
        db=db,
        registration_session=registration_session,
    )


@router.delete('/cancel-registration', response_model=StatusResponseSchema)
async def cancel_registration(
    registration_session: Registration = Depends(get_registration_session),
    db: AsyncSession = Depends(get_db),
):
    ''' Deletes completed registration sessions data '''
    return await registration_service.cancel_registration(
        db=db,
        registration_session=registration_session,
    )

