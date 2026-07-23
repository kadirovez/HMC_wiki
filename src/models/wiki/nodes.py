
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    DateTime,
    func,
    Enum as SQLEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.utils.default_title import default_title
from src.core.database import Base


class NodeType(str, Enum):
    PAGE = "page"
    SECTION = "section"
    FOLDER = "folder"
    FILE = "file"

class Node(Base):
    __tablename__ = "nodes"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    parent_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("nodes.id", ondelete="CASCADE"),
        nullable=True,
    )

    type: Mapped[NodeType] = mapped_column(
        SQLEnum(NodeType),
        index=True,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        default=default_title,
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(255),
        index=True,
        nullable=False,
    )

    order_index: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    created_at : Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    updated_at : Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relations

    parent = relationship(
        "Node",
        remote_side="Node.id",
        back_populates="children",
    )

    children = relationship(
        "Node",
        back_populates="parent",
        passive_deletes=True,
    )

    file_content = relationship(
        "FileContent",
        back_populates="node",
        uselist=False,
        cascade="all, delete-orphan",
    )
