
from datetime import timedelta, datetime, timezone

from src.core.settings import settings
from src.models.wiki.editor_session import EditorSession


def is_expired(editor_session : EditorSession):
    anchor = editor_session.last_autosaved_at or editor_session.created_at
    ttl = timedelta(minutes=settings.stale_ttl)
    return anchor + ttl < datetime.now(timezone.utc)
