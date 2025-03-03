"""Модуль для роутера аккаунтов."""

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import src.accounts.schemas as account_schemas
from src import dependencies
from src.accounts.services import AccountService
from src.users.models import UserModel

account_router = APIRouter(prefix="/accounts", tags=["accounts"])


@account_router.get(path="")
async def get_all_accounts_route(
    session: AsyncSession = Depends(dependencies.get_session),
    user: UserModel = Depends(dependencies.get_current_user),
) -> list[account_schemas.AccountGetSchema]:
    """
    Получить все аккаунты пользователя.

    Доступно только авторизованному пользвоателю.
    """

    return await AccountService.get_all_by_user_id(session, user_id=user.id)


@account_router.get(
    path="/{user_id}",
    dependencies=[
        Depends(dependencies.get_current_admin),
    ],
)
async def get_all_accounts_by_user_id_route(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(dependencies.get_session),
) -> list[account_schemas.AccountGetSchema]:
    """
    Получить все аккаунты пользователя.

    Доступно только администратору.
    """

    return await AccountService.get_all_by_user_id(session, user_id=user_id)
