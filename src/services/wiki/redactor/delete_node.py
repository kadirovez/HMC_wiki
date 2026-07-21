
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Node


async def delete_node(
        db: AsyncSession,
        node_id: UUID,
) -> None:
    """
    Deletes node and all its descendants (sections, folders, files)
    via ON DELETE CASCADE on parent_id, including nested file_content.
    """

    node = await db.get(Node, node_id)
    if node is None:
        raise HTTPException(
            status_code=404,
            detail="Node not found",
        )

    await db.delete(node)
    await db.commit()
