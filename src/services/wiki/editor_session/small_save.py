
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.wiki.editor_session import get_active_session
from src.crud.wiki.helpers import is_expired
from src.models.wiki.editor_session import EditorSession
from src.schemas.wiki.editor import SaveRequest


async def small_save(
        db: AsyncSession,
        user_id: int,
        data: SaveRequest,
) -> EditorSession:
    """
    Makes small saves in editor session. Frontend calls this function whenever it needs
    """
    editor_session = await get_active_session(db, data.node_id)

    if editor_session is None:
        raise HTTPException(
            status_code=404,
            detail="No active editing session for this node",
        )

    if editor_session.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Node is being edited by another user"
        )

    if is_expired(editor_session):
        raise HTTPException(
            status_code=409,
            detail="Editing session has expired, please restart it"
        )

    editor_session.draft_content = data.content
    editor_session.last_autosaved_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(editor_session)
    return editor_session
