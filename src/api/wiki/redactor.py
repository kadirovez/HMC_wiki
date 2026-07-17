
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.deps.database import get_db
from src.deps.permission import require_role
from src.models import UserRole, User
from src.models.wiki.nodes import Node
from src.schemas.wiki.nodes_schemas import NodeCreate, NodeTitleUpdate
from src.services.wiki.redactor import redactor_service

router = APIRouter(prefix="/redact", tags=["redact"])


@router.post("/node")
async def create_node(
        data: NodeCreate,
        db: AsyncSession = Depends(get_db),
        _current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    """
    Creates folder, auto generates slug, current user is needed to check for permission
    """
    return await redactor_service.create_node(
        data=data,
        db=db,
    )


@router.patch("/node")
async def edit_node_title(
        data: NodeTitleUpdate,
        db: AsyncSession = Depends(get_db),
        _current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    """
    Edit node title, and generates new slug
    """
    return await redactor_service.edit_node_title(
        data=data,
        db=db,
    )


@router.patch("/file")
async def edit_file(
        db: AsyncSession = Depends(get_db),
        _current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    """
    Edit file, if file title was changed, generates new slug
    """
    return await redactor_service.edit_file()
