
from typing import TYPE_CHECKING

from src.models.auth.base import SessionDatabaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


if TYPE_CHECKING:
    from src.models.auth.user import User

class Main(SessionDatabaseModel):
    ''' Main model '''

    __tablename__ = 'main'

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey('user.id', ondelete='CASCADE'),
        nullable=True,
        index=True
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates='main'
    )

