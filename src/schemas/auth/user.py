
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from src.core.settings import settings
from src.models import UserRole
from src.schemas.fields import USERNAME_FIELD, NAME_FIELD, EMAIL_FIELD


class UserCreate(BaseModel):
    ''' Schema for creating user '''

    username : USERNAME_FIELD
    first_name:  NAME_FIELD
    last_name : NAME_FIELD
    password : str = Field(..., min_length=1, max_length=255)
    email : EMAIL_FIELD
    email_is_confirmed : bool = Field(default=False)
    is_active : bool = Field(default=False)


class UserUpdate(BaseModel):
    ''' Schema for updating user '''

    password : Optional[str] = Field(default=None, min_length=settings.password_min_length)
    bad_password_count : Optional[int] = None
    first_name : Optional[str] = None
    last_name : Optional[str] = None
    email : Optional[EmailStr] = None
    email_confirmed : Optional[bool] = None
    email_code_limit : Optional[int] = None
    is_active : Optional[bool] = None
    is_locked : Optional[bool] = None
    bad_password_time : Optional[datetime] = None


class UserRoleUpdate(BaseModel):
    """ Schema for updating user roles """

    role : UserRole


class UserListResponse(BaseModel):
    """ Schema for receiving base info of user """
    id: int
    username: USERNAME_FIELD
    first_name : NAME_FIELD
    last_name : NAME_FIELD
    role : UserRole

    model_config = ConfigDict(from_attributes=True)
