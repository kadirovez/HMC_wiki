
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.schemas.base import BaseResponseSchema
from src.schemas.fields import (
    USERNAME_FIELD,
    NAME_FIELD,
    PASSWORD_FIELD,
    EMAIL_FIELD,
    OTP_CODE_FIELD,
)


class RegistrationProfileRequest(BaseModel):
    ''' 1st step: personal info '''

    first_name: NAME_FIELD
    last_name: NAME_FIELD
    username: USERNAME_FIELD
    email: EMAIL_FIELD


class RegistrationPasswordRequest(BaseModel):
    ''' 2nd step: password '''

    password: PASSWORD_FIELD


class RegistrationConfirmPasswordRequest(BaseModel):
    ''' 3nd step: confirm password '''

    confirm_password: PASSWORD_FIELD


class RegistrationEmailOTPRequest(BaseModel):
    ''' Step 4th : confirm otp '''

    email_otp: OTP_CODE_FIELD


class RegistrationUpdate(BaseModel):
    ''' Field for updating registration session '''

    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    password_is_confirmed: Optional[bool] = None
    email_is_confirmed: Optional[bool] = None
    email_code_sent: Optional[str] = None
    email_code_id: Optional[str] = None
    email_code_expire_at: Optional[datetime] = None
    is_completed: Optional[bool] = None


class RegistrationCompleteResponse(BaseResponseSchema):
    ''' Response schema, might be unuseful '''

    user_id: int
