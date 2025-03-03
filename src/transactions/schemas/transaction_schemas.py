"""Модуль для Pydantic схем транзакций."""

import uuid

from pydantic import BaseModel


class TransactionSchema(BaseModel):
    """Схема транзакции."""

    id: str
    account_id: uuid.UUID | str
    user_id: uuid.UUID | str
    amount: int
    signature: str

    class Config:
        from_attributes = True
        json_encoders = {uuid.UUID: str}
