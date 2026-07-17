
from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator

from src.models.wiki.nodes import NodeType


class NodeCreate(BaseModel):
    parent_id : UUID | None = None
    type: NodeType
    title: str | None = None

    @field_validator("parent_id", mode="before")
    @classmethod
    def empty_string_to_none(cls, value):
        if value == "":
            return None
        return value

class NodeTitleUpdate(BaseModel):
    node_id: UUID
    title: str

class ShortNodeResponse(BaseModel):
    id: UUID
    slug: str
    title: str

    model_config = ConfigDict(from_attributes=True)
