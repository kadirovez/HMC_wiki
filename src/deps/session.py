
from fastapi import HTTPException, Depends, Request, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeVar

from src.core.settings import settings
from src.core.database import Base
from src.crud.auth.base import CRUDSessionBase
from src.crud.auth.login import login_crud
from src.crud.auth.main import main_crud
from src.crud.auth.register import registration_crud
from src.crud.wiki.redact import redact_crud
from src.deps.database import get_db
from src.utils.ip_address import get_ip
from src.utils.jwt_token import decode_access_token



bearer_scheme = HTTPBearer()
ModelType = TypeVar("ModelType", bound=Base)


async def _get_session_from_token(
        request : Request,
        credentials : HTTPAuthorizationCredentials,
        db : AsyncSession,
        crud : CRUDSessionBase
):
    """
    Generic helper to get session from JWT token.
    This centralizes all the common logic between login and registration.
    """
    # Decode jwt token
    payload = decode_access_token(credentials.credentials)

    # Extract session token
    session_token = payload.get('session')
    if not session_token:
        raise HTTPException(
            status_code=401,
            detail='Invalid token payload'
        )

    # Get ip for validation
    request_ip = get_ip(request)
    token_ip = payload.get('ip_address')

    # Checks if ip exists (if ip check is enabled in settings)
    if settings.ip_check_enabled and token_ip is None:
        raise HTTPException(
            status_code=401,
            detail='Token missing ip address'
        )

    # Comparing two ips
    if settings.ip_check_enabled and request_ip and token_ip:
        if request_ip != token_ip:
            raise HTTPException(
                status_code=401,
                detail='Token ip mismatch'
            )

    session_obj = await crud.get_by_session(db, session=session_token)

    if not session_obj:
        raise HTTPException(
            status_code=401,
            detail='Session was not found'
        )

    return session_obj


async def get_token_from_cookie(
        access_token: str | None = Cookie(
            default=None,
        ),
) -> str :
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
        )
    return access_token


async def get_login_session(
        request : Request,
        credentials : HTTPAuthorizationCredentials = Depends(bearer_scheme),
        db : AsyncSession = Depends(get_db)
):
    ''' Gets login session via jwt '''
    return await _get_session_from_token(request, credentials, db, login_crud)


async def get_registration_session(
        request : Request,
        credentials : HTTPAuthorizationCredentials = Depends(bearer_scheme),
        db: AsyncSession = Depends(get_db)
):
    ''' Gets registration sesion via jwt '''
    return await _get_session_from_token(request, credentials, db, registration_crud)


async def get_main_session(
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        db: AsyncSession = Depends(get_db),
):
    ''' Gets main session via jwt '''
    return await _get_session_from_token(request, credentials, db, main_crud)


async def get_redact_session(
        request: Request,
        credentials : HTTPAuthorizationCredentials = Depends(bearer_scheme),
        db: AsyncSession = Depends(get_db),
):
    """ Gets edit session for commiting changes in files """
    return await _get_session_from_token(request, credentials, db, redact_crud)
