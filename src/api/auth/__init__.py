
from .login import router as login_router
from .registration import router as registration_router
from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

auth_router.include_router(login_router)
auth_router.include_router(registration_router)
