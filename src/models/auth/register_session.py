
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, String, DateTime

from src.models.auth.base import SessionAuthDataBase


class Registration(SessionAuthDataBase):

    __tablename__ = 'registration'

    username: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
    )

    first_name: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
    )

    last_name: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    password: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    password_is_confirmed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        server_default='false',
    )

    email_is_confirmed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        server_default='false',
    )

    email_code_sent: Mapped[str | None] = mapped_column(
        String(6),
        nullable=True,
    )

    email_code_id: Mapped[str | None] = mapped_column(
        String(32),
        nullable=True,
    )

    email_code_expire_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        default=None,
        nullable=True,
    )
