
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.schemas.base import BaseResponseSchema
from src.schemas.fields import USERNAME_FIELD, EMAIL_FIELD, PASSWORD_FIELD, OTP_CODE_FIELD

# class LoginIdentificationRequest(BaseModel):
#
#     login: str


class LoginUsernameRequest(BaseModel):
    ''' Username login : step 1'''

    username: USERNAME_FIELD


class LoginEmailRequest(BaseModel):
    ''' Email login: step 1'''

    email: EMAIL_FIELD


class LoginConfirmEmailRequest(BaseModel):
    ''' Username login: step 2, check email after masking it '''

    email: EMAIL_FIELD


class LoginPasswordRequest(BaseModel):
    ''' Both login methods: step 3, password '''

    password: PASSWORD_FIELD


class LoginEmailOTPRequest(BaseModel):
    ''' Both login methods: step 4, check email otp code '''

    email_otp: OTP_CODE_FIELD


class LoginMaskedEmailResponse(BaseResponseSchema):
    ''' Step 2 response: shows masked email '''

    masked_email: str

class LoginUpdate(BaseModel):
    ''' Update login schema '''

    user_id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    password_is_validated: Optional[bool] = None
    email_matched: Optional[bool] = None
    email_is_confirmed: Optional[bool] = None
    email_code_sent: Optional[str] = None
    email_code_id: Optional[str] = None
    email_code_expire_at: Optional[datetime] = None
    is_completed: Optional[bool] = None


class LoginFinishResponse(BaseResponseSchema):
    ''' Token response schema '''

    access_token: str
    token_type: str = "bearer"

