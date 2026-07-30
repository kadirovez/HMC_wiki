
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.wiki.nodes import Node, NodeType


async def _get_descendants(
        db: AsyncSession,
        root_id: UUID,
) -> list[Node] :
    """
    Recursive CTE: fetches all descendant nodes of root_id (any depth).
    """

    base = (
        select(Node.id, Node.parent_id, Node.type, Node.title, Node.slug, Node.order_index)
        .where(Node.parent_id == root_id)
        .cte(name="descendants", recursive=True)
    )

    descendants = base.union_all(
        select(Node.id, Node.parent_id, Node.type, Node.title, Node.slug, Node.order_index)
        .join(base, Node.parent_id == base.c.id)
    )

    statement = select(Node).join(descendants, Node.id == descendants.c.id)
    result = await db.scalars(statement)
    return list(result.all())


def _build_tree(
        root: Node,
        nodes: list[Node],
) -> dict:
    """
    Builds a nested dict tree from a flat list of nodes, rooted at `root`.
    """
    children_by_parent: dict[UUID, list[Node]] = {}
    for node in nodes:
        children_by_parent.setdefault(node.parent_id, []).append(node)

    for children in children_by_parent.values():
        children.sort(key=lambda n: n.order_index)

    def to_dict(node: Node) -> dict:
        return {
            "id":node.id,
            "title":node.title,
            "order_index":node.order_index,
            "slug":node.slug,
            "type":node.type,
            "children":[to_dict(child) for child in children_by_parent.get(node.id, [])]
        }

    return to_dict(root)


async def get_page_tree(
        db:AsyncSession,
        slug: str,
) -> dict :
    """
    Returns the full node tree (sections, folders, files) for a single page.
    Identified by its slug, as a nested dict.
    """
    statement = select(Node).where(
        Node.slug == slug,
        Node.type == NodeType.PAGE
    )
    page = await db.scalar(statement)

    if page is None:
        raise HTTPException(
            status_code=404,
            detail="Page not found",
        )

    descendants = await _get_descendants(db, page.id)
    return _build_tree(page, descendants)

