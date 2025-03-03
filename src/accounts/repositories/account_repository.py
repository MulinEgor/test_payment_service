"""Модуль для репозиториев аккаунтов."""

import src.accounts.schemas as account_schemas
from src.accounts.models import AccountModel
from src.base_repository import BaseRepository


class AccountRepository(
    BaseRepository[
        AccountModel,
        account_schemas.AccountCreateSchema,
        account_schemas.AccountCreateSchema,
    ]
):
    """
    Основной репозиторий для работы с моделью AccountModel.
    Наследуется от базового репозитория.
    """

    model = AccountModel
