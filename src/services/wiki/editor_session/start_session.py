
from datetime import timedelta, datetime, timezone
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import settings
from src.crud.wiki.editor_session import get_active_session
from src.models.wiki.editor_session import EditorSession


def _is_expired(editor_session):
    anchor = editor_session.last_autosaved_at or editor_session.created_at
    ttl = timedelta(minutes=settings.stale_ttl)
    return anchor + ttl < datetime.now(timezone.utc)


async def start_session(
        db: AsyncSession,
        node_id: UUID,
        user_id: UUID,
) -> EditorSession:
    """
    Creates new edit session in case if the old one was not closed properly
    Otherwise it intercepts existing session
    """
    existing = await get_active_session(db, node_id)

    # Case 1: creating new session
    if existing is None:
        editor_session = EditorSession(
            node_id=node_id,
            user_id=user_id,
        )
        db.add(editor_session)
        try:
            await db.commit()
        except IntegrityError:
            # race condition: someone managed to create a session
            # between our SELECT and INSERT
            await db.rollback()
            raise HTTPException(
                status_code=409,
                detail="Node is currently being edited by another user",
            )
        await db.refresh(editor_session)
        return editor_session

    # Case 2: the session belongs to the user, we just extend the TTL
    if existing.user_id == user_id:
        existing.last_autosaved_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(existing)
        return existing

    # Case 3: The session belongs to someone else, but has expired fue to TTL - we intercept its string
    if _is_expired(existing):
        existing.user_id = user_id,
        existing.draft_content = {},
        existing.last_autosaved_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(existing)
        return existing

    raise HTTPException(
        status_code=409,
        detail="Node is currently being edited by another user",
    )

