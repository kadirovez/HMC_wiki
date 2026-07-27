
import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Node
from src.schemas.wiki.editor import FilePresignedRequest
from src.services.wiki.editor_session.s3_utils import generate_presigned_put_url


ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/webp", "image/gif"}
ALLOWED_VIDEO_TYPES = {"video/mp4", "video/webm", "video/quicktime"}
PRESIGN_TTL = 3600

async def generate_upload_url(
        db: AsyncSession,
        data: FilePresignedRequest,
) -> dict:

    # Check if node exists
    node = await db.get(Node, data.node_id)
    if node is None:
        raise HTTPException(
            status_code=404,
            detail="Node was not found"
        )

    is_image = data.content_type in ALLOWED_IMAGE_TYPES
    is_video = data.content_type in ALLOWED_VIDEO_TYPES

    # File type is not supported
    if not (is_image or is_video):
        raise HTTPException(
            status_code=415,
            detail="Only images or videos are allowed"
        )

    ext = data.filename.rsplit(".", 1)[-1] if "." in data.filename else "bin"
    media_type = "images" if is_image else "videos"
    key = f"{media_type}/{data.node_id}/{uuid.uuid4()}.{ext}"

    upload_url = await generate_presigned_put_url(
        key=key,
        content_type=data.content_type,
        expires_in=PRESIGN_TTL,
    )

    return {"key": key, "upload_url": upload_url, "type": "image" if is_image else "video"}
