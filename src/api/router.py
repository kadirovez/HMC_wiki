
from fastapi import APIRouter

from src.api.auth.login import router as login_router
from src.api.auth.registration import router as registration_router
from src.api.admin import admin_router

api_router = APIRouter()
api_router.include_router(registration_router)
api_router.include_router(login_router)
api_router.include_router(admin_router)
