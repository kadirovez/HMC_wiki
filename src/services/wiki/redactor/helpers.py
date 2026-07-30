
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Node


# async def get_max_order_index(
#         db: AsyncSession,
#         parent_id: UUID | None,
# ) -> int:
#     """ Gets max order index from all nodes of one selected parent """
#     statement = select(func.max(Node.order_index)).where(Node.parent_id == parent_id)
#     max_order = await db.scalar(statement)
#     return (max_order or -1) +1


async def get_max_order_index(
        db: AsyncSession,
        parent_id: UUID | None,
) -> int:
    """ Gets max order index from all nodes of one selected parent """
    condition = (
        Node.parent_id.is_(None) if parent_id is None
        else Node.parent_id == parent_id
    )
    statement = select(func.coalesce(func.max(Node.order_index), -1)).where(condition)
    max_order = await db.scalar(statement)
    return max_order + 1
