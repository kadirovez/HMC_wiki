
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.deps.database import get_db
from src.deps.permission import require_role
from src.models import User, UserRole
from src.schemas.wiki.editor import EditorStatus, SaveRequest, MediaPresignedRequest
from src.services.wiki.editor_session import editor_service

router = APIRouter(prefix="/edit", tags=["edit"])



@router.get("/")
async def start_session(
        node_id: UUID,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(require_role(UserRole.ADMIN))
):
    """ Creates new session or intercepts an existing one with an expired TTL """
    return await editor_service.start_session(
        db=db,
        user_id=user.id,
        node_id=node_id,
    )


@router.get("/editor-status", response_model=EditorStatus)
async def get_status(
        node_id : UUID,
        db: AsyncSession = Depends(get_db),
        _current_user: User = Depends(require_role(UserRole.ADMIN))
) -> EditorStatus:
    """ Checks if the node is locked, without intercepting it """
    return await editor_service.get_status(
        db=db,
        node_id=node_id,
    )


@router.patch("/editor")
async def small_save(
        data: SaveRequest,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(require_role(UserRole.ADMIN)),
):
    """ Autosaves draft in editor session """
    return await editor_service.small_save(
        db=db,
        user_id=user.id,
        data=data,
    )


@router.patch("/editor-save")
async def save(
        data: SaveRequest,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(require_role(UserRole.ADMIN)),
):
    """ Saves the draft to the main file """
    return await editor_service.save(
        db=db,
        data=data,
        user_id=user.id,
    )


@router.post("/media")
async def generate_upload_url(
        data: MediaPresignedRequest,
        db: AsyncSession = Depends(get_db),
        _current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """ Returns url to upload file to storage """
    return await editor_service.generate_upload_url(
        db=db,
        data=data,
    )


@router.delete("/editor")
async def end_session(
        node_id: UUID,
        db: AsyncSession = Depends(get_db),
        user: User = Depends(require_role(UserRole.ADMIN)),
):
    """ снятие лока + чистка orphan-картинок из черновика """
    return await editor_service.end_session(
        db=db,
        node_id=node_id,
        user_id=user.id,
    )
