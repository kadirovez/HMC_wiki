
from src.crud.auth.base import CRUDSessionBase
from src.models.wiki.editor_session import EditorSession
from src.schemas.auth.base import CreateSessionSchema
from src.schemas.wiki.redactor import EditorUpdate


class CRUDEdit(CRUDSessionBase[EditorSession, CreateSessionSchema, EditorUpdate]):
    pass


editor_crud = CRUDEdit(EditorSession)
