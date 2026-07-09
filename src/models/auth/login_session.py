
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models.auth.base import SessionAuthDataBase


class Login(SessionAuthDataBase):

    __tablename__ = 'login'

    login_method: Mapped[str | None] = mapped_column(
        String(16),
        nullable=True,
    )

    user_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey('user.id'),
        nullable=True,
        index=True,
    )

    username: Mapped[str | None] = mapped_column(
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

    password_is_validated: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        server_default='false',
    )

    # Field for matching email on masking check step
    email_matched: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        server_default='false',
    )

    # Confirming email on otp step
    email_is_confirmed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        server_default='false',
    )

    email_code_sent: Mapped[str] = mapped_column(
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

