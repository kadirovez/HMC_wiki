
from datetime import timedelta, datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import settings
from src.crud.auth.base import CRUDSessionBase
from src.schemas.addons import Token
from src.schemas.auth.base import CreateSessionSchema
from src.utils.generator import generate_string
from src.utils.jwt_token import create_access_token


class SessionService:
    async def start_session(
        self,
        db: AsyncSession,
        ip_address: str,
        crud: CRUDSessionBase,
        create_schema: type[CreateSessionSchema],
    ) -> Token:
        ''' Creates a new session and returns jwt token with info in it '''

        session_token = generate_string(256, digits=True, uppercase=True, lowercase=True)
        access_token_expire_date = timedelta(minutes=settings.access_token_expire_minutes)

        # Create session
        await crud.create(
            db=db,
            obj_in=create_schema(
                ip_address=ip_address,
                session=session_token
            )
        )

        access_token = create_access_token(
            data={
                'session':session_token,
                'ip_address':ip_address,
            },
            expires_delta=access_token_expire_date
        )

        return Token(
            access_token=access_token,
            token_type='bearer',
            expires_in=str(datetime.now(timezone.utc) + access_token_expire_date)
        )

# Singleton instance
session_service = SessionService()

