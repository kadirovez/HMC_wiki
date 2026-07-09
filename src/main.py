
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.router import api_router
from src.core.database import close_db, init_db
from src.core.settings import settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(
    debug=settings.debug,
    title=settings.app_name,
    version=settings.app_version,
    docs_url='/docs' if settings.debug else None,
    openapi_url='/openapi.json' if settings.debug else None,
    lifespan=lifespan,
)

app.include_router(api_router, prefix='/api/v1')
