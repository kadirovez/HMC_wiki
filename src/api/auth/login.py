
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.login import login_crud
from src.deps.database import get_db
from src.deps.session import get_login_session
from src.models.auth.login_session import Login
from src.schemas.addons import Token
from src.schemas.auth.base import CreateSessionSchema
from src.schemas.auth.login import (
    LoginPasswordRequest,
    LoginEmailRequest,
)
from src.services.auth.login import login_service
from src.services.session import session_service
from src.utils.ip_address import get_ip

router = APIRouter(prefix='/login', tags=['login'])


@router.get('/start', response_model=Token)
async def start_login(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    ''' Starts login session '''
    return await session_service.start_session(
        db=db,
        ip_address=get_ip(request),
        crud=login_crud,
        create_schema=CreateSessionSchema,
    )

@router.post('/validae_email')
async def validate_email(
        obj_in: LoginEmailRequest,
        login_session: Login = Depends(get_login_session),
        db: AsyncSession = Depends(get_db)
):
    return await login_service.validate_email(
        db=db,
        login_session=login_session,
        obj_in=obj_in
    )


@router.post('/password')
async def submit_password(
    obj_in: LoginPasswordRequest,
    login_session: Login = Depends(get_login_session),
    db: AsyncSession = Depends(get_db),
):
    ''' Validates password for both flows '''
    return await login_service.validate_password(
        db=db,
        login_session=login_session,
        obj_in=obj_in,
    )


@router.post('/complete-login')
async def complete_login(
        request:Request,
        login_session: Login = Depends(get_login_session),
        db: AsyncSession = Depends(get_db),
):
    return await login_service.complete_login(
        request=request,
        db=db,
        login_session=login_session,
    )


@router.delete('/cancel')
async def cancel_login(
    login_session: Login = Depends(get_login_session),
    db: AsyncSession = Depends(get_db),
):
    return await login_service.cancel_login(
        db=db,
        login_session=login_session,
    )
