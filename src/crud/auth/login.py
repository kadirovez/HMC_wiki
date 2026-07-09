
from src.crud.auth.base import CRUDSessionBase
from src.models.auth.login_session import Login
from src.schemas.auth.base import CreateSessionSchema
from src.schemas.auth.login import LoginUpdate


class CRUDLogin(CRUDSessionBase[Login, CreateSessionSchema, LoginUpdate]):
    ''' CRUD operations for login session '''

    reset_values = {
        "login_method": None,
        "user_id": None,
        "username": None,
        "email": None,
        "password": None,
        "password_is_validated": False,
        "email_matched": False,
        "email_is_confirmed": False,
        "email_code_sent": None,
        "email_code_id": None,
        "email_code_expire_at": None,
        "is_completed": False,
    }


login_crud = CRUDLogin(Login)
