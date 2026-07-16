
from uuid import UUID

from slugify import slugify
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.wiki.nodes import Node


async def generate_slug(
    session: AsyncSession,
    title: str,
    parent_id: UUID | None,
    exclude_node_id: UUID | None = None,
) -> str:

    base_slug = slugify(title, max_length=100) or "node"
    slug = base_slug
    counter = 1

    while True:
        query = select(Node.id).where(
            Node.parent_id == parent_id, Node.slug == slug
        )
        if exclude_node_id is not None:
            query = query.where(Node.id != exclude_node_id)

        existing = await session.scalar(query)
        if existing is None:
            return slug

        counter += 1
        slug = f"{base_slug}-{counter}"
