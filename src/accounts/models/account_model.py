"""Модуль для SQLAlchemy моделей аккаунтов."""

import uuid

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.transactions.models import TransactionModel


class AccountModel(Base):
    """Модель аккаунта."""

    __tablename__ = "accounts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        comment="Идентификатор аккаунта.",
    )
    balance: Mapped[int] = mapped_column(
        default=0,
        comment="Баланс аккаунта.",
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        comment="Идентификатор пользователя.",
    )

    user: Mapped["UserModel"] = relationship(
        back_populates="accounts",
        foreign_keys=[user_id],
    )
    transactions: Mapped[list[TransactionModel]] = relationship(
        back_populates="account",
        lazy="joined",
    )
