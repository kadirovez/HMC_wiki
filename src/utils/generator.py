
from datetime import datetime, timedelta, timezone
from typing import Tuple
import secrets
import string


def generate_string(
        length: int = 16,
        digits: bool = True,
        uppercase: bool = False,
        lowercase: bool = False,
        symbols: bool = False
) -> str:
    ''' Generate cryptographically secure random string '''

    # Build character pool from flags
    character_sets = {
        'digits': string.digits if digits else "",
        'uppercase': string.ascii_uppercase if uppercase else "",
        'lowercase': string.ascii_lowercase if lowercase else "",
        'symbols': string.punctuation if symbols else "",
    }

    character_pool = ''.join(character_sets.values())

    # If no character set is selected, return empty string
    if not character_pool:
        return ''

    # Ensure at least one character from each selected set
    required_chars = [
        secrets.choice(charset)
        for charset in character_sets.values()
        if charset
    ]

    # Fill the remaining length with random choices
    remaining_length = length - len(required_chars)
    if remaining_length > 0:
        required_chars += [
            secrets.choice(character_pool)
            for _ in range(remaining_length)
        ]

    # Cryptographically secure shuffle using Fisher-Yates algorithm
    for i in range(len(required_chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        required_chars[i], required_chars[j] = required_chars[j], required_chars[i]

    return ''.join(required_chars)

def generate_otp(length: int = 4, timeout: int = 5) -> Tuple[str, str, datetime]:
    ''' Generate otp '''
    otp_code = generate_string(length=length, digits=True)
    otp_code_id = generate_string(8, digits=True, uppercase=True)
    otp_expire_at = datetime.now(timezone.utc) + timedelta(minutes=timeout)

    return otp_code, otp_code_id, otp_expire_at
