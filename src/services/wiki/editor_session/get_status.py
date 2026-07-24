
from datetime import timedelta
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import settings
from src.crud.wiki.editor_session import get_active_session
from src.crud.wiki.helpers import is_expired
from src.schemas.wiki.editor import EditorStatus


async def get_status(
        db: AsyncSession,
        node_id: UUID,
) -> EditorStatus:
    existing = await get_active_session(db, node_id)

    if existing is None:
        return EditorStatus(is_locked=False)

    if is_expired(existing):
        return EditorStatus(is_locked=False)

    return EditorStatus(
        is_locked=True,
        locked_by=existing.user_id,
        locked_until=existing.last_autosaved_at + timedelta(minutes=settings.stale_ttl)
    )
