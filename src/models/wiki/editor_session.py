
from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, Boolean, Index, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseDataModel


class EditorSession(BaseDataModel):
    __tablename__ = "editor_session"

    node_id: Mapped[UUID] = mapped_column(
        ForeignKey("nodes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    draft_content: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )

    is_discarded: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="False",
    )

    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="False",
    )

    last_autosaved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    node = relationship("Node")
    user = relationship("User")

    __table_args__ = (
        Index(
            "uq_active_session_per_node",
            "node_id",
            unique=True,
            postgresql_where=(is_completed.is_(False)),
        ),
    )
