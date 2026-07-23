from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.deps.database import get_db
from src.deps.permission import require_role
from src.models import User, UserRole
from src.services.wiki.editor_session import editor_service

router = APIRouter(prefix="/edit", tags=["edit"])



@router.post("/")
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


@router.get("/editor-status")
async def get_status():
    """ залочен ли файл и кем (без захвата) """
    return await editor_service.get_status()


@router.patch("/editor")
async def small_save():
    """ черновик в editing_cd src/services/sessions, без ревизий """
    return await editor_service.small_save()


@router.post("/editor")
async def save():
    """ commit в file_contents + revision + чистка orphan-картинок """
    return await editor_service.save()


@router.post("/img")
async def upload_image():
    """ — загрузка картинки в S3, возврат key + presigned url """
    return await editor_service.upload_image()


@router.delete("/editor")
async def end_session():
    """ снятие лока + чистка orphan-картинок из черновика """
    return await editor_service.end_session()
