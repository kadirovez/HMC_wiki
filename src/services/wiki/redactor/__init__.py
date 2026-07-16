
from edit_file import edit_file
from edit_node_title import edit_node_title
from create_node import create_node

class RedactorService:
    edit_file = staticmethod(edit_file)
    edit_node_title = staticmethod(edit_node_title)
    create_node = staticmethod(create_node)

redactor_service = RedactorService()
