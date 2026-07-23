
from .get_status import get_status
from .start_session import start_session
from .end_session import end_session
from .save import save
from .small_save import small_save
from .upload_image import upload_image

class EditorService():
    get_status = staticmethod(get_status)
    start_session = staticmethod(start_session)
    end_session = staticmethod(end_session)
    save = staticmethod(save)
    small_save = staticmethod(small_save)
    upload_image = staticmethod(upload_image)


editor_service = EditorService()

