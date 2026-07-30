
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.wiki.file_content import FileContent
from src.models.wiki.nodes import NodeType, Node
from src.schemas.wiki.nodes_schemas import NodeCreate
from src.services.wiki.redactor.helpers import get_max_order_index
from src.utils.default_title import default_title
from src.utils.generate_slug import generate_slug


ALLOWED_PARENT_TYPES : dict[NodeType, set[NodeType | None]] = {
    NodeType.PAGE : {None},
    NodeType.SECTION : {NodeType.PAGE},
    NodeType.FOLDER : {NodeType.SECTION, NodeType.FOLDER},
    NodeType.FILE : {NodeType.SECTION, NodeType.FOLDER},
}


async def create_node(
        db: AsyncSession,
        data: NodeCreate,
) -> Node:
    """
    Creates node with provided data, including type, title and parent node.
    If the created object was a file, it automatically creates empty file_content.
    Title generates automatically if not specified.
    The slug is also generated automatically from the provided title
    """
    parent : Node | None = None

    if data.parent_id is not None:
        parent = await db.get(Node, data.parent_id)
        if parent is None:
            raise HTTPException(
                status_code=401,
                detail="Parent node not found"
            )

    parent_type = parent.type if parent else None
    allowed_parents = ALLOWED_PARENT_TYPES.get(data.type, set())

    # Validates node inheritance rules
    if parent_type not in allowed_parents:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Node of type '{data.type.value}' cannot be created "
                f"under parent of type '{parent_type.value if parent_type else "root"}'"
            )
        )

    title = data.title or default_title()
    slug = await generate_slug(db, title, data.parent_id)
    order_index = await get_max_order_index(db, data.parent_id)

    node = Node(
        parent_id=data.parent_id,
        type=data.type,
        title=title,
        slug=slug,
        order_index=order_index
    )

    db.add(node)
    await db.flush()

    if data.type == NodeType.FILE:
        db.add(
            FileContent(
                node_id=node.id,
                content={}
            )
        )

    await db.commit()
    await db.refresh(node)
    return node
