
from datetime import datetime

def default_title() -> str:

    return f"Created at {datetime.now():%H:%M %d/%m/%Y}"

