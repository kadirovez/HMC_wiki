
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class EditorStatus(BaseModel):
    is_locked: bool
    locked_by: int | None = None
    locked_until: datetime | None = None


class SaveRequest(BaseModel):
    node_id: UUID
    content: dict


class FilePresignedRequest(BaseModel):
    node_id: UUID
    filename: str
    content_type: str
