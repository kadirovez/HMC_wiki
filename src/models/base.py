
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime,func, Boolean
from datetime import datetime
from src.core.database import Base

class BaseDataModel(Base):

    __abstract__ = True

    id : Mapped[int] = mapped_column(
        primary_key=True,
        index=True
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

    is_active : Mapped[bool] = mapped_column(
        Boolean,
        server_default='True',
        nullable=False
    )

    is_locked : Mapped[bool] = mapped_column(
        Boolean,
        server_default='False',
        default=False,
        nullable=False
    )