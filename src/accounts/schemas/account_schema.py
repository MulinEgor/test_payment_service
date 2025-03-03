"""Модуль для Pydantic схем аккаунтов"""

import uuid

from pydantic import BaseModel, Field

import src.transactions.schemas as transaction_schemas


# MARK: Account
class AccountCreateSchema(BaseModel):
    """Pydantic схема для создания аккаунта."""

    id: uuid.UUID | None = Field(
        default=None,
        description="Идентификатор аккаунта.",
    )
    balance: int = Field(description="Баланс аккаунта.")
    user_id: uuid.UUID = Field(description="Идентификатор пользователя.")

    class Config:
        json_encoders = {uuid.UUID: str}


class AccountGetSchema(AccountCreateSchema):
    """Pydantic схема для получения аккаунта."""

    transactions: list[transaction_schemas.TransactionSchema] = Field(
        description="Транзакции аккаунта.",
    )
