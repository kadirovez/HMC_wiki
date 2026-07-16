
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from src.models.wiki.nodes import NodeType


class NodeCreate(BaseModel):
    parent_id : UUID | None = None
    type: NodeType
    title: str | None = None


class NodeTitleUpdate(BaseModel):
    node_id: UUID
    title: str

class ShortNodeResponse(BaseModel):
    node_id: UUID
    slug: str
    title: str

    model_config = ConfigDict(from_attributes=True)
