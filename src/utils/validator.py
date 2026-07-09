
from src.core.settings import settings

import re

def validate_password_policy(password : str) -> str:
    '''
    Password validator, checks if the password meets all the requirements .
        Returns ValueError if an error occurs.
    '''

    errors = []

    if settings.password_require_uppercase and not re.search(r'[A-Z]', password):
        errors.append('at least one uppercase letter')

    if settings.password_require_lowercase and not re.search(r'[a-z]', password):
        errors.append('at least one lowercase letter')

    if settings.password_require_digit and not re.search(r'\d', password):
        errors.append('at least one digit')

    if settings.password_require_symbol and not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/`~;]', password):
        errors.append('at least one special symbol')

    if errors:
        raise ValueError(
            f'Password must contain: {','.join(errors)}'
        )
    return password

