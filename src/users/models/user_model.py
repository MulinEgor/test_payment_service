"""Модуль для SQLAlchemy моделей пользователей."""

import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.accounts.models import AccountModel
from src.constants import CURRENT_TIMESTAMP_UTC
from src.database import Base
from src.transactions.models import TransactionModel


class UserModel(Base):
    """SQLAlchemy модель пользователя."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4,
        primary_key=True,
        comment="Уникальный идентификатор пользователя.",
    )
    email: Mapped[str] = mapped_column(
        unique=True,
        comment="Электронная почта пользователя.",
    )
    hashed_password: Mapped[str] = mapped_column(
        comment="Хэшированный пароль пользователя.",
    )
    full_name: Mapped[str] = mapped_column(
        comment="Полное имя пользователя.",
    )
    is_admin: Mapped[bool] = mapped_column(
        default=False,
        comment="Является ли пользователь администратором.",
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=CURRENT_TIMESTAMP_UTC,
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=CURRENT_TIMESTAMP_UTC,
        onupdate=CURRENT_TIMESTAMP_UTC,
    )

    accounts: Mapped[list[AccountModel]] = relationship(
        back_populates="user",
    )
    transactions: Mapped[list[TransactionModel]] = relationship(
        back_populates="user",
    )
