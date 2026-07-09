
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.schemas.auth.base import CreateSessionSchema


class MainCreate(CreateSessionSchema):
    ''' Base schema for creating Main Session '''

    user_id: int

class MainUpdate(BaseModel):
    ''' Upadate schema for main, all fields are optional '''

    user_id: Optional[int] = None

class MainInDBBase(BaseModel):

    id : int
    session : str
    user_id : Optional[int]
    created_at : datetime
    updated_at : datetime

    model_config = ConfigDict(from_attributes=True)

