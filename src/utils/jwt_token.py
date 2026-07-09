
from datetime import timedelta, datetime, timezone
from fastapi import HTTPException
from typing import Any
import jwt

from src.core.settings import settings


def create_access_token(
        data: dict[str, Any],
        expires_delta: timedelta | None = None,
) -> str:
    ''' Creates JWT token '''

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=settings.secret_key,
        algorithm=settings.algorithm
    )

    return encoded_jwt



def decode_access_token(
        token: str,
) -> dict[str, Any] | None:
    ''' Decodes jwt token '''

    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.secret_key,
            algorithms=[settings.algorithm],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail='Token expired'
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail='Invalid Token'
        )

