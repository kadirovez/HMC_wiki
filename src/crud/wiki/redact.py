
from src.crud.auth.base import CRUDSessionBase
from src.models.wiki.redact_session import RedactSession
from src.schemas.auth.base import CreateSessionSchema
from src.schemas.wiki.redactor import RedactorUpdate


class CRUDRedact(CRUDSessionBase[RedactSession, CreateSessionSchema, RedactorUpdate]):
    pass

redact_crud = CRUDRedact(RedactSession)
