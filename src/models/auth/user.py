
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.settings import settings
from src.models.base import BaseDataModel


class User(BaseDataModel):

    __tablename__ = 'user'

    username: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        nullable=False,
        index=True,
    )

    first_name: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        index=True,
    )

    last_name: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        index=True,
    )

    # Email
    email : Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    email_confirmed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default='false',
    )

    email_code_limit: Mapped[int] = mapped_column(
        Integer,
        default=settings.user_email_code_limit,
        nullable=False,
    )

    bad_email_code_time: Mapped[datetime | None] = mapped_column(
        DateTime,
        default=None,
        nullable=True,
    )

    # Password
    password : Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    password_change: Mapped[datetime | None] = mapped_column(
        DateTime,
        default=None,
        nullable=True,
    )

    bad_password_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    bad_password_time: Mapped[datetime | None] = mapped_column(
        DateTime,
        default=None,
        nullable=True,
    )

    main: Mapped["Main | None"] = relationship(
        'Main',
        back_populates='user',
        uselist=False,
        cascade='all, delete-orphan',
    )
