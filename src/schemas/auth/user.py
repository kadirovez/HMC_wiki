
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from src.core.settings import settings
from src.schemas.fields import USERNAME_FIELD, NAME_FIELD, EMAIL_FIELD


class UserCreate(BaseModel):
    ''' Schema for creating user '''

    username: USERNAME_FIELD
    first_name: NAME_FIELD
    last_name: NAME_FIELD
    password: str = Field(..., min_length=1, max_length=255)
    email: EMAIL_FIELD
    email_is_confirmed: bool = Field(default=False)
    is_active: bool = Field(default=False)


class UserUpdate(BaseModel):
    ''' Schema for updating user '''

    password: Optional[str] = Field(default=None, min_length=settings.password_min_length)
    bad_password_count: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    email_confirmed: Optional[bool] = None
    email_code_limit: Optional[int] = None
    is_active: Optional[bool] = None
    is_locked: Optional[bool] = None
    bad_password_time : Optional[datetime] = None
