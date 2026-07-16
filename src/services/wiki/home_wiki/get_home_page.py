
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.wiki.nodes import Node, NodeType


async def get_home_page(
        db: AsyncSession,
):
    statement = (
        select(Node)
        .where(Node.type == NodeType.PAGE)
        .order_by(Node.order_index)
    )

    result = await db.scalars(statement)
    return list(result.all())

