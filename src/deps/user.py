from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.auth.user import user_crud
from src.deps.database import get_db
from src.deps.session import get_main_session
from src.models import Main, User


async def get_current_user(
        main_session: Main = Depends(get_main_session),
        db: AsyncSession = Depends(get_db),
) -> User:
    """ Retrieves user from jwt token """
    if not main_session.user_id:
        raise HTTPException(status_code=401, detail='Invalid session')

    return await user_crud.get(db=db, id=main_session.user_id)

