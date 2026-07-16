
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.wiki.nodes import Node
from src.schemas.wiki.nodes_schemas import NodeTitleUpdate
from src.utils.generate_slug import generate_slug


async def edit_node_title(
        db: AsyncSession,
        data: NodeTitleUpdate,
) -> Node :
    """
    This function lets you change the title of any node
    """
    node: Node | None = await db.get(Node, data.node_id)
    if node is None:
        raise HTTPException(
            status_code=404,
            detail="Node not found"
        )

    node.title = data.title
    node.slug = await generate_slug(
        db,
        data.title,
        node.parent_id,
        exclude_node_id=node.id
    )

    await db.commit()
    await db.refresh(node)
    return node

