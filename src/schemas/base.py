
from pydantic import ConfigDict, BaseModel
from typing import TypeVar

T = TypeVar('T')

class StatusResponseSchema(BaseModel):
    ''' Base schema for status sessions  '''
    status : bool

class BaseResponseSchema(BaseModel):
    ''' Turns orm into dict view '''
    model_config = ConfigDict(from_attributes=True)
