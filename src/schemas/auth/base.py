
from pydantic import BaseModel, Field


class CreateSessionSchema(BaseModel):
    ''' Base schema for creating session'''

    ip_address: str = Field(
        ...,
        max_length=15,
        description='Client IP address'
    )

    session: str = Field(
        ...,
        min_length=64,
        max_length=256,
        description='Session token'
    )
