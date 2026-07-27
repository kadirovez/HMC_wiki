
from .get_status import get_status
from .start_session import start_session
from .end_session import end_session
from .save import save
from .small_save import small_save
from .upload_image import generate_upload_url

class EditorService():
    get_status = staticmethod(get_status)
    start_session = staticmethod(start_session)
    end_session = staticmethod(end_session)
    save = staticmethod(save)
    small_save = staticmethod(small_save)
    generate_upload_url = staticmethod(generate_upload_url)


editor_service = EditorService()

