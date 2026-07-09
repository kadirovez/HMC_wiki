
import re

def mask_email(email: str) -> str:
    """Mask email address: fa********@*****.com"""

    match = re.match(r"([^@]+)@([^@.]+)\.([a-zA-Z]+)$", email)

    if not match:
        raise ValueError('Invalid email format')

    local_part, domain, tld = match.groups()
    masked_local = local_part[:2] + "*" * (len(local_part) - 2)
    masked_domain = "*" * len(domain)
    return f"{masked_local}@{masked_domain}.{tld}"
