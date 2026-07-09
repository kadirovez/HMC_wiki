
from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import BaseDataModel


class SessionDatabaseModel(BaseDataModel):

    __abstract__ = True

    ip_address: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True,
        index=True,
    )

    session: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        index=True,
    )


class SessionAuthDataBase(SessionDatabaseModel):

    __abstract__ = True

    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        server_default='false',
    )

