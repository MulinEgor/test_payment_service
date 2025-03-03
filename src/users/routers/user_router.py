"""Модуль для маршрутов пользователей."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

import src.users.schemas as user_schemas
from src import dependencies
from src.users.models import UserModel
from src.users.services import UserService

user_router = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)


# MARK: Get
@user_router.get(
    "/me",
    summary="Получить данные текущего пользователя.",
    status_code=status.HTTP_200_OK,
    response_model=user_schemas.UserReadSchema,
)
async def get_current_user_route(
    user: UserModel = Depends(dependencies.get_current_user),
) -> user_schemas.UserReadSchema:
    """
    Получить данные текущего пользователя.

    Доступно авторизованному пользователю.
    """

    return user_schemas.UserReadSchema.model_validate(user)


@user_router.get(
    "/{id}",
    summary="Получить данные пользователя по ID.",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(dependencies.get_current_user)],
    response_model=user_schemas.UserReadSchema,
)
async def get_user_by_id_route(
    id: str,
    session: AsyncSession = Depends(dependencies.get_session),
) -> user_schemas.UserReadSchema:
    """
    Получить данные пользователя по id.

    Доступно авторизованному пользователю.
    """

    return await UserService.get_by_id(session, id)


@user_router.get(
    "",
    summary="Администратор. Получить список пользователей.",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(dependencies.get_current_admin)],
    response_model=user_schemas.UserListReadSchema,
)
async def get_users_by_admin_route(
    query_params: user_schemas.UsersQuerySchema = Query(),
    session: AsyncSession = Depends(dependencies.get_session),
) -> user_schemas.UserListReadSchema:
    """
    Получить список пользователей и их общее количество
    с фильтрацией по query параметрам, отличным от None.

    Доступно только администратору.
    """

    return await UserService.get(session, query_params)


# MARK: Post
@user_router.post(
    "",
    summary="Администратор. Создать нового пользователя.",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(dependencies.get_current_admin)],
)
async def create_user_by_admin_route(
    data: user_schemas.UserCreateAdminSchema,
    session: AsyncSession = Depends(dependencies.get_session),
) -> user_schemas.UserReadAdminSchema:
    """
    Создать нового пользователя.

    Доступно только администратору.
    """

    return await UserService.create(session, data)


# MARK: Patch
@user_router.patch(
    "/me",
    summary="Обновить данные текущего пользователя.",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(dependencies.get_current_user)],
    response_model=user_schemas.UserReadSchema,
)
async def update_user_route(
    data: user_schemas.UserUpdateSchema,
    session: AsyncSession = Depends(dependencies.get_session),
    user: UserModel = Depends(dependencies.get_current_user),
) -> user_schemas.UserReadSchema:
    """
    Обновить данные текущего пользователя.

    Доступно авторизованному пользователю.
    """

    return await UserService.update(session, user.id, data)


# MARK: Put
@user_router.put(
    "/{id}",
    summary="Администратор. Обновить данные пользователя.",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(dependencies.get_current_admin)],
)
async def update_user_by_admin_route(
    id: str,
    data: user_schemas.UserUpdateAdminSchema,
    session: AsyncSession = Depends(dependencies.get_session),
) -> user_schemas.UserReadAdminSchema:
    """
    Обновить данные пользователя.

    Доступно только администратору.
    """

    return await UserService.update(session, id, data)


# MARK: Delete
@user_router.delete(
    "/{id}",
    summary="Администратор. Удалить пользователя.",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(dependencies.get_current_admin)],
)
async def delete_user_by_admin_route(
    id: str,
    session: AsyncSession = Depends(dependencies.get_session),
) -> None:
    """
    Удалить пользователя.

    Доступно только администратору.
    """

    await UserService.delete(session, id)
