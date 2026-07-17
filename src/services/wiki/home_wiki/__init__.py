
from .get_home_page import get_home_page
from .get_page_tree import get_page_tree
from .get_file import get_file

class WikiServices:
    get_home_page = staticmethod(get_home_page)
    get_page_tree = staticmethod(get_page_tree)
    get_file = staticmethod(get_file)

wiki_services = WikiServices()
