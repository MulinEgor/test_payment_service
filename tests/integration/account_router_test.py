"""Тесты для роутера аккаунтов."""

import httpx
from fastapi import status

import src.accounts.schemas as account_schemas
import src.auth.schemas as auth_schemas
from src import constants
from src.accounts.models import AccountModel
from src.accounts.routers import account_router
from src.users.models import UserModel
from tests.integration.conftest import BaseTestRouter


class TestAccountRouter(BaseTestRouter):
    """Класс для тестирования роутера account_router."""

    router = account_router

    # MARK: Get
    async def test_get_all_accounts(
        self,
        router_client: httpx.AsyncClient,
        user_db: UserModel,
        user_jwt_tokens: auth_schemas.JWTGetSchema,
        account_db: AccountModel,
    ):
        """Проверка получения всех аккаунтов пользователя."""

        response = await router_client.get(
            url="/accounts",
            headers={constants.AUTH_HEADER_NAME: user_jwt_tokens.access_token},
        )

        assert response.status_code == status.HTTP_200_OK

        data = [
            account_schemas.AccountGetSchema(**account) for account in response.json()
        ]

        assert data[0].id == account_db.id
        assert data[0].balance == account_db.balance
        assert str(data[0].user_id) == user_db.id

    async def test_get_all_accounts_by_user_id(
        self,
        router_client: httpx.AsyncClient,
        user_db: UserModel,
        admin_jwt_tokens: auth_schemas.JWTGetSchema,
        account_db: AccountModel,
    ):
        """Проверка получения всех аккаунтов пользователя администратором."""

        response = await router_client.get(
            url=f"/accounts/{user_db.id}",
            headers={constants.AUTH_HEADER_NAME: admin_jwt_tokens.access_token},
        )

        assert response.status_code == status.HTTP_200_OK

        data = [
            account_schemas.AccountGetSchema(**account) for account in response.json()
        ]

        assert data[0].id == account_db.id
        assert data[0].balance == account_db.balance
        assert str(data[0].user_id) == user_db.id
