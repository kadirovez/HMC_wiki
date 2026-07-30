
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
        # When creating a Page node, you dont specify a parent_id,
        # causing an empty string to be returned as 'Null',
        # which triggers an error.
        # This method converts Null to None, as it needed for database 
        if value == "":
            return None
        return value


class NodeTitleUpdate(BaseModel):
    node_id: UUID
    title: str

class NodeMove(BaseModel):
    node_id: UUID
    new_parent_id: UUID | None = None
    new_order_index: int | None = None


class NodeDelete(BaseModel):
    node_id: UUID


class ShortNodeResponse(BaseModel):
    id: UUID
    slug: str
    title: str

    model_config = ConfigDict(from_attributes=True)
