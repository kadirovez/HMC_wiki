
from typing import Any

def normalize_lowercase(value : Any) -> str:
    ''' Normalize to lowercase and delete all spaces '''
    if isinstance(value, str):
        return value.strip().lower()
    return value

def normalize_uppercase(value : Any) -> str:
    ''' Normalize to uppercase and delete all spaces '''
    if isinstance(value, str):
        return value.strip().upper()
    return value


def normalize_capitalize(value : Any) -> str:
    ''' Capitalize first symbol, and delete all spaces'''
    if isinstance(value, str):
        return value.strip().capitalize()
    return value
