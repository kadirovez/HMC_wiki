
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.wiki.editor_session import EditorSession


async def get_active_session(
        db: AsyncSession,
        node_id: UUID,
) -> (
        EditorSession | None) :
    result = await db.execute(
        select(EditorSession).where(
            EditorSession.node_id == node_id,
            EditorSession.is_completed.is_(False),
        )
    )
    return result.scalar_one_or_none()
