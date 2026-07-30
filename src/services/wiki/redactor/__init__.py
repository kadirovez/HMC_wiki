
from .edit_node_title import edit_node_title
from .create_node import create_node
from .delete_node import delete_node
from .move_node import move_node

class RedactorService:
    edit_node_title = staticmethod(edit_node_title)
    create_node = staticmethod(create_node)
    delete_node = staticmethod(delete_node)
    move_node = staticmethod(move_node)

redactor_service = RedactorService()
