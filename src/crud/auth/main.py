
from src.crud.auth.base import CRUDSessionBase
from src.models.auth.main import Main
from src.schemas.auth.main import MainCreate, MainUpdate


class CRUDMain(CRUDSessionBase[Main, MainCreate, MainUpdate]):
    ''' CRUD operations for main sessions '''


main_crud = CRUDMain(Main)
