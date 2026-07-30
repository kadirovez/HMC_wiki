
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Node
from src.schemas.wiki.nodes_schemas import NodeMove
from src.services.wiki.redactor.create_node import ALLOWED_PARENT_TYPES
from src.services.wiki.redactor.helpers import get_max_order_index


async def _shift_order_indexes(
        db: AsyncSession,
        parent_id: UUID | None,
        from_index: int,
        exclude_node_id: UUID,
) -> None:
    """ Shifts 'order_index' of siblings, starting from 'from_index' to make room for the insertion """
    statement = (
        select(Node).where(
            Node.parent_id == parent_id,
            Node.order_index >= from_index,
            Node.id != exclude_node_id,
        )
    )

    result = await db.scalars(statement)
    siblings = result.all()

    for sibling in siblings:
        sibling.order_index += 1


async def _is_self_or_descendant(
        db: AsyncSession,
        node_id: UUID,
        candidate_id: UUID,
) -> bool:
    """ Checks whether candidate_id is the node 'node_id' itself or one of its descendants """
    if node_id == candidate_id:
        return True

    statement = select(Node.id).where(Node.parent_id == node_id)
    result = await db.scalars(statement)
    children_ids = result.all()

    for child_id in children_ids:
        if await _is_self_or_descendant(db, child_id, candidate_id):
            return True

    return False


async def move_node(
        db: AsyncSession,
        data: NodeMove,
) -> Node:
    """
    Moves node to a new parent (or keeps the same parent if only order_index needs to be changed)
    Validates type nesting rules and prevents moving node into itself or into its own subtree.
    If order_index is not specified, the node is added as the last child of the new parent.
    """
    node = await db.get(Node, data.node_id)

    if Node is None:
        raise HTTPException(
            status_code=403,
            detail="Node not found"
        )

    new_parent: Node | None = None

    if data.new_parent_id is not None:
        new_parent = await db.get(Node, data.new_parent_id)

        if new_parent is None:
            raise HTTPException(
                status_code=403,
                detail="Parent node not found"
            )

    if new_parent is not None and await _is_self_or_descendant(db, data.node_id, data.new_parent_id):
        raise HTTPException(
            status_code=400,
            detail="Cannot move node into itself or its own descendant",
        )

    new_parent_type = new_parent.type if new_parent else None
    allowed_parents = ALLOWED_PARENT_TYPES.get(node.type, set())

    if new_parent_type not in allowed_parents:
        raise HTTPException(
            status_code=403,
            detail=(
                f"Node of type '{node.type.value}' cannot be moved "
                f"under parent of type '{new_parent_type.value if new_parent_type else "root"}'"
            )
        )

    if data.new_order_index is None:
        target_index = await get_max_order_index(db, data.new_parent_id)
    else:
        target_index = data.new_order_index
        await _shift_order_indexes(
            db=db,
            parent_id=data.new_parent_id,
            from_index=target_index,
            exclude_node_id=data.node_id,
        )

    node.parent_id = data.new_parent_id
    node.order_index = target_index

    await db.commit()
    await db.refresh(node)
    return node

