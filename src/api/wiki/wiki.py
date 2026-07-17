
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.deps.database import get_db
from src.deps.user import get_current_user
from src.schemas.wiki.nodes_schemas import ShortNodeResponse
from src.services.wiki.home_wiki import wiki_services

router = APIRouter(prefix="/wiki", tags=["wiki"])


@router.get("/", response_model=list[ShortNodeResponse])
async def get_home_page(
        db: AsyncSession = Depends(get_db),
        _current_user = Depends(get_current_user)
):
    """
    Opens the home page with main menu
    Loads all available pages for further exploration
    """
    return await wiki_services.get_home_page(db)


@router.get("/{slug}")
async def get_page_tree(
        slug: str,
        db: AsyncSession = Depends(get_db),
        _current_user = Depends(get_current_user),
):
    """
    Get full directory by page (sections, folders and files)
    """
    return await wiki_services.get_page_tree(
        slug=slug,
        db=db,
    )


@router.get("/file/{slug}")
async def get_file(
        slug: str,
        parent_id: UUID,
        db: AsyncSession = Depends(get_db),
        _current_user = Depends(get_current_user),
):
    """
    Get file content
    """
    return await wiki_services.get_file(
        slug=slug,
        parent_id=parent_id,
        db=db,
    )

