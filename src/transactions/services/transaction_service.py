"""Модуль для сервисов транзакций."""

import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import src.accounts.schemas as account_schemas
import src.transactions.schemas as transaction_schemas
from src import exceptions, utils
from src.accounts.services import AccountService
from src.settings import settings
from src.transactions.repositories import TransactionRepository


class TransactionService:
    """Сервис транзакций."""

    # MARK: Utils
    @classmethod
    async def check_transaction_signature(
        cls,
        data: transaction_schemas.TransactionSchema,
    ) -> bool:
        """
        Проверка подписи транзакции.

        Args:
            data (TransactionSchema):
                Данные транзакции.

        Returns:
            bool: True, если подпись транзакции корректна, иначе False.
        """

        signature = utils.get_hash(
            str(data.account_id)
            + str(data.amount)
            + data.id
            + str(data.user_id)
            + settings.TRANSACTION_SIGNATURE_SECRET
        )

        return signature == data.signature

    # MARK: Create
    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        data: transaction_schemas.TransactionSchema,
    ) -> transaction_schemas.TransactionSchema:
        """
        Создать транзакцию в БД.

        Args:
            session (AsyncSession): Сессия для работы с базой данных.
            data (TransactionSchema):
                Данные для создания транзакции.

        Returns:
            TransactionSchema: Добавленная транзакция.

        Raises:
            TransactionAlreadyExistsException: Транзакция уже существует.
            TransactionInvalidSignatureException: Некорректная подпись транзакции.
        """

        # Проверка подписи транзакции
        if not await cls.check_transaction_signature(data):
            raise exceptions.TransactionInvalidSignatureException()

        # Если аккаунт не существует, то создаем его
        try:
            account = await AccountService.get(session=session, id=data.account_id)

        except exceptions.AccountNotFoundException:
            schema = account_schemas.AccountCreateSchema(
                id=data.account_id,
                balance=0,
                user_id=data.user_id,
            )
            account = await AccountService.create(session=session, data=schema)

        try:
            # Добавление транзакции в БД
            transaction = await TransactionRepository.add(
                session=session,
                obj_in=data,
            )
            await session.commit()

        except IntegrityError as ex:
            raise exceptions.TransactionConflictException(exc=ex)

        # Обновить баланс счета
        await AccountService.update_balance(
            session=session,
            id=account.id,
            new_balance=account.balance + data.amount,
        )

        return transaction_schemas.TransactionSchema.model_validate(transaction)

    # MARK: Get
    @classmethod
    async def get_all_by_user_id(
        cls,
        session: AsyncSession,
        user_id: uuid.UUID,
    ) -> list[transaction_schemas.TransactionSchema]:
        """
        Поиск транзакций по ID пользователя.

        Args:
            session (AsyncSession): Сессия для работы с базой данных.
            user_id (uuid.UUID): ID пользователя.

        Returns:
            list[TransactionSchema]: Найденные транзакции.

        Raises:
            TransactionNotFoundException: Транзакция не найдена.
        """

        # Поиск транзакции в БД
        transactions_db = await TransactionRepository.find_all(
            session=session,
            user_id=user_id,
        )

        if transactions_db is None:
            raise exceptions.TransactionNotFoundException()

        return [
            transaction_schemas.TransactionSchema.model_validate(transaction)
            for transaction in transactions_db
        ]
