
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class EditorStatus(BaseModel):

    is_locked: bool
    locked_by: UUID | None = None
    locked_until: datetime | None = None
    