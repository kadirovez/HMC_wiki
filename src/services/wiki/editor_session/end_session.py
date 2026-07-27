
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.wiki.editor_session import get_active_session


async def end_session(
        db: AsyncSession,
        node_id: UUID,
        user_id: int,
):
    editor_session = await get_active_session(db, node_id)

    if editor_session is None:
        return

    if editor_session.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Node is being edited by another user"
        )

    await db.delete(editor_session)
    await db.commit()
