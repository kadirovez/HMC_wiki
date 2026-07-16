
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class FileContent(Base):
    __tablename__ = "file_contents"

    node_id: Mapped[UUID] = mapped_column(
        ForeignKey("nodes.id", ondelete="CASCADE"),
        primary_key=True,
    )

    content: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
        nullable=True,
    )

    # Relations

    node = relationship("Node", back_populates="file_content")
