"""Модуль для роутера транзакций."""

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import src.transactions.schemas as transaction_schemas
from src import dependencies
from src.transactions.services import TransactionService
from src.users.models import UserModel

transaction_router = APIRouter(prefix="/transactions", tags=["transactions"])


@transaction_router.get(path="")
async def get_all_transactions_route(
    session: AsyncSession = Depends(dependencies.get_session),
    user: UserModel = Depends(dependencies.get_current_user),
) -> list[transaction_schemas.TransactionSchema]:
    """
    Получить все транзакции пользователя.

    Доступно только авторизованному пользвоателю.
    """

    return await TransactionService.get_all_by_user_id(session, user_id=user.id)


@transaction_router.get(
    path="/{user_id}",
    dependencies=[Depends(dependencies.get_current_admin)],
)
async def get_all_transactions_by_user_id_route(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(dependencies.get_session),
) -> list[transaction_schemas.TransactionSchema]:
    """
    Получить все транзакции пользователя.

    Доступно только администратору.
    """

    return await TransactionService.get_all_by_user_id(session, user_id=user_id)


@transaction_router.post(
    path="",
    dependencies=[Depends(dependencies.get_current_admin)],
    response_model=transaction_schemas.TransactionSchema,
)
async def create_transaction_route(
    data: transaction_schemas.TransactionSchema,
    session: AsyncSession = Depends(dependencies.get_session),
) -> transaction_schemas.TransactionSchema:
    """
    Создать транзакцию.

    Доступно только администратору.
    """

    return await TransactionService.create(session, data)
