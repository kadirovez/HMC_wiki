
from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, Boolean, Index, Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import SessionAuthDataBase


class RedactSession(SessionAuthDataBase):
    __tablename__ = "redact_session"

    node_id: Mapped[UUID] = mapped_column(
        ForeignKey("nodes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
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

    is_completed = Column(
        Boolean,
        nullable=False,
        default=False
    )

    last_autosaved_at: Mapped[datetime | None] = mapped_column(
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
