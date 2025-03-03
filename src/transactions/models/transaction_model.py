"""Модуль для SQLAlchemy моделей транзакций."""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.accounts.models.account_model import AccountModel
    from src.users.models.user_model import UserModel


class TransactionModel(Base):
    """Модель транзакции."""

    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(
        primary_key=True,
        comment="Идентификатор транзакции.",
    )
    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("accounts.id"),
        comment="Идентификатор аккаунта.",
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        comment="Идентификатор пользователя.",
    )
    amount: Mapped[int] = mapped_column(
        comment="Сумма транзакции.",
    )
    signature: Mapped[str] = mapped_column(
        comment="Подпись транзакции.",
    )

    account: Mapped["AccountModel"] = relationship(
        back_populates="transactions",
        foreign_keys=[account_id],
    )
    user: Mapped["UserModel"] = relationship(
        back_populates="transactions",
        foreign_keys=[user_id],
    )
