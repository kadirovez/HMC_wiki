
from fastapi import APIRouter

router = APIRouter(prefix="/edit", tags=["edit"])



@router.post("/")
async def start_session():
    """ Захват pessimistic lock, создание/возврат сессии """
    pass


@router.get("/")
async def get_status():
    """ залочен ли файл и кем (без захвата) """
    pass


@router.patch("/")
async def small_save():
    """ черновик в editing_cd src/services/sessions, без ревизий """
    pass


@router.post("/")
async def save():
    """ commit в file_contents + revision + чистка orphan-картинок """
    pass


@router.post("/")
async def upload_image():
    """ — загрузка картинки в S3, возврат key + presigned url """
    pass


@router.delete("/")
async def end_session():
    """ снятие лока + чистка orphan-картинок из черновика """
    pass
