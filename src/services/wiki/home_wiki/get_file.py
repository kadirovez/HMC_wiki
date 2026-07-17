
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.wiki.file_content import FileContent
from src.models.wiki.nodes import Node, NodeType


async def get_file(
        db: AsyncSession,
        slug: str,
        parent_id: UUID | None = None,
) -> dict :
    """
    Returns file metadata with its JSONB content.
    If parent_id is not provided and multiple files share the same slug
    under different parents, raises a 409 asking to disambiguate.
    """

    statement = select(Node).where(
        Node.slug == slug,
        Node.type == NodeType.FILE,
    )

    if parent_id is not None:
        statement = statement.where(Node.parent_id == parent_id)

    result = await db.scalars(statement)
    nodes = list(result.all())

    if not nodes:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    if len(nodes) > 1:
        raise HTTPException(
            status_code=409,
            detail="Multiple files match this slug, specify parent_id",
        )

    node = nodes[0]

    file_content = await db.get(FileContent, node.id)
    if file_content is None:
        raise HTTPException(
            status_code=404,
            detail="File content was not found for this page"
        )

    return {
        "id": node.id,
        "title": node.title,
        "slug": node.slug,
        "parent_id": node.parent_id,
        "content": file_content.content,
    }
