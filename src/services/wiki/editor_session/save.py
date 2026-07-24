
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.wiki.editor_session import get_active_session
from src.crud.wiki.helpers import is_expired
from src.models import FileContent
from src.schemas.wiki.editor import SaveRequest


async def save(
        db: AsyncSession,
        data: SaveRequest,
        user_id: int,
) -> FileContent:

    editor_session = await get_active_session(db, data.node_id)

    if editor_session is None:
        raise HTTPException(
            status_code=404,
            detail="No active editing sessions for this node"
        )

    if editor_session.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Node is being edited by another user"
        )

    if is_expired(editor_session):
        raise HTTPException(
            status_code=409,
            detail="Session expired, please restart it"
        )

    result = await db.execute(
        select(FileContent).where(FileContent.node_id == data.node_id)
    )
    file_content = result.scalar_one_or_none()
    if file_content is None:
        raise HTTPException(
            status_code=404,
            detail="File content not found for this node",
        )

    # Save to main project
    file_content.content = data.content

    editor_session.draft_content = data.content
    editor_session.last_autosaved_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(file_content)
    return file_content

