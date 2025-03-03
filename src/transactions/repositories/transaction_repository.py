"""Модуль для репозиториев транзакций."""

import src.transactions.schemas as transaction_schemas
from src.base_repository import BaseRepository
from src.transactions.models import TransactionModel


class TransactionRepository(
    BaseRepository[
        TransactionModel,
        transaction_schemas.TransactionSchema,
        transaction_schemas.TransactionSchema,
    ]
):
    """
    Основной репозиторий для работы с моделью TransactionModel.
    Наследуется от базового репозитория.
    """

    model = TransactionModel
