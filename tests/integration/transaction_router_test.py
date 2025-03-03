"""Тесты для роутера транзакций."""

import httpx
from fastapi import status

import src.auth.schemas as auth_schemas
import src.transactions.schemas as transaction_schemas
from src import constants
from src.transactions.models import TransactionModel
from src.transactions.routers import transaction_router
from src.users.models import UserModel
from tests.integration.conftest import BaseTestRouter


class TestTransactionRouter(BaseTestRouter):
    """Класс для тестирования роутера transaction_router."""

    router = transaction_router

    # MARK: Get
    async def test_get_all_transactions(
        self,
        router_client: httpx.AsyncClient,
        user_db: UserModel,
        user_jwt_tokens: auth_schemas.JWTGetSchema,
        transaction_db: TransactionModel,
    ):
        """Проверка получения всех транзакций пользователя."""

        response = await router_client.get(
            url="/transactions",
            headers={constants.AUTH_HEADER_NAME: user_jwt_tokens.access_token},
        )

        assert response.status_code == status.HTTP_200_OK

        data = [
            transaction_schemas.TransactionSchema(**transaction)
            for transaction in response.json()
        ]

        assert data[0].id == transaction_db.id
        assert data[0].account_id == str(transaction_db.account_id)
        assert data[0].signature == transaction_db.signature
        assert data[0].amount == transaction_db.amount
        assert str(data[0].user_id) == user_db.id

    async def test_get_all_transactions_by_user_id(
        self,
        router_client: httpx.AsyncClient,
        user_db: UserModel,
        admin_jwt_tokens: auth_schemas.JWTGetSchema,
        transaction_db: TransactionModel,
    ):
        """Проверка получения всех транзакций пользователя администратором."""

        response = await router_client.get(
            url=f"/transactions/{user_db.id}",
            headers={constants.AUTH_HEADER_NAME: admin_jwt_tokens.access_token},
        )

        assert response.status_code == status.HTTP_200_OK

        data = [
            transaction_schemas.TransactionSchema(**transaction)
            for transaction in response.json()
        ]

        assert data[0].id == transaction_db.id
        assert data[0].account_id == str(transaction_db.account_id)
        assert data[0].signature == transaction_db.signature
        assert data[0].amount == transaction_db.amount
        assert str(data[0].user_id) == user_db.id

    async def test_create_transaction(
        self,
        router_client: httpx.AsyncClient,
        user_db: UserModel,
        admin_jwt_tokens: auth_schemas.JWTGetSchema,
        transaction_create_data: transaction_schemas.TransactionSchema,
    ):
        """Проверка создания транзакции администратором."""

        response = await router_client.post(
            url="/transactions",
            headers={constants.AUTH_HEADER_NAME: admin_jwt_tokens.access_token},
            json=transaction_create_data.model_dump(),
        )

        assert response.status_code == status.HTTP_200_OK

        data = transaction_schemas.TransactionSchema(**response.json())

        assert data.id == transaction_create_data.id
        assert data.account_id == str(transaction_create_data.account_id)
        assert data.signature == transaction_create_data.signature
        assert data.amount == transaction_create_data.amount
        assert str(data.user_id) == user_db.id
