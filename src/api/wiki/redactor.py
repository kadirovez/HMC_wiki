
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.deps.database import get_db
from src.deps.permission import require_role
from src.models import UserRole, User
from src.schemas.wiki.nodes_schemas import NodeCreate, NodeTitleUpdate, NodeDelete, NodeMove
from src.services.wiki.redactor import redactor_service

router = APIRouter(prefix="/files", tags=["redact"])


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


@router.patch("/node/move")
async def move_node(
        data: NodeMove,
        db: AsyncSession = Depends(get_db),
        _current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """
    Moves node to a new parent (or reorders within the same parent),
    validates node type nesting rules and prevents moving a node into itself or its own descendant
    """
    return await redactor_service.move_node(
        db=db,
        data=data,
    )


@router.delete("/node")
async def delete_node(
        data: NodeDelete,
        db: AsyncSession = Depends(get_db),
        _current_user : User = Depends(require_role(UserRole.ADMIN)),
):
    """
    Deletes node, and all descendants
    """
    await redactor_service.delete_node(
        node_id=data.node_id,
        db=db
    )

