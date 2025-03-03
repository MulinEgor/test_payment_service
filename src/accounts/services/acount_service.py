"""Модуль для сервиса аккаунтов."""

import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import src.accounts.schemas as account_schemas
import src.transactions.schemas as transaction_schemas
from src import exceptions
from src.accounts.repositories import AccountRepository


class AccountService:
    """Сервис для работы с аккаунтами."""

    # MARK: Create
    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        data: account_schemas.AccountCreateSchema,
    ) -> account_schemas.AccountGetSchema:
        """
        Создать аккаунт в БД.

        Args:
            session (AsyncSession): Сессия для работы с базой данных.
            data (AccountCreateSchema):
                Данные для создания аккаунта.

        Returns:
            AccountGetSchema: Добавленный аккаунт.

        Raises:
            AccountAlreadyExistsException: Аккаунт уже существует.
        """

        try:
            # Добавление аккаунта в БД
            account = await AccountRepository.add(
                session=session,
                obj_in=data,
            )
            await session.commit()
            return account_schemas.AccountGetSchema.model_validate(account)

        except IntegrityError as ex:
            raise exceptions.AccountConflictException(exc=ex)

    # MARK: Get
    @classmethod
    async def get(
        cls,
        session: AsyncSession,
        id: uuid.UUID,
    ) -> account_schemas.AccountGetSchema:
        """
        Поиск аккаунта по ID.

        Args:
            session (AsyncSession): Сессия для работы с базой данных.
            id (uuid.UUID): ID аккаунта.

        Returns:
            AccountGetSchema: Найденный аккаунт.

        Raises:
            AccountNotFoundException: Аккаунт не найден.
        """

        # Поиск аккаунта в БД
        account_db = await AccountRepository.find_one_or_none(
            session=session,
            id=id,
        )

        if account_db is None:
            raise exceptions.AccountNotFoundException()

        transactions = [
            transaction_schemas.TransactionSchema.model_validate(transaction)
            for transaction in account_db.__dict__.pop("transactions")
        ]

        return account_schemas.AccountGetSchema(
            **account_db.__dict__,
            transactions=transactions,
        )

    @classmethod
    async def get_all_by_user_id(
        cls,
        session: AsyncSession,
        user_id: uuid.UUID,
    ) -> list[account_schemas.AccountGetSchema]:
        """
        Поиск аккаунта по ID пользователя.

        Args:
            session (AsyncSession): Сессия для работы с базой данных.
            user_id (uuid.UUID): ID пользователя.

        Returns:
            list[AccountGetSchema]: Найденные аккаунты.

        Raises:
            AccountNotFoundException: Аккаунт не найден.
        """

        # Поиск аккаунта в БД
        account_db = await AccountRepository.find_all(
            session=session,
            user_id=user_id,
        )

        if account_db is None:
            raise exceptions.AccountNotFoundException()

        result = []
        for account in account_db:
            transactions = [
                transaction_schemas.TransactionSchema.model_validate(transaction)
                for transaction in account.__dict__.pop("transactions")
            ]
            result.append(
                account_schemas.AccountGetSchema(
                    **account.__dict__,
                    transactions=transactions,
                )
            )

        return result

    # MARK: Update
    @classmethod
    async def update_balance(
        cls,
        session: AsyncSession,
        id: uuid.UUID,
        new_balance: int,
    ) -> None:
        """
        Обновление баланса аккаунта.

        Args:
            session (AsyncSession): Сессия для работы с базой данных.
            id (uuid.UUID): ID аккаунта.
            new_balance (int): Новый баланс аккаунта.

        Raises:
            AccountNotFoundException: Аккаунт не найден.
        """

        account = await cls.get(session=session, id=id)

        account.balance = new_balance
        await session.commit()
