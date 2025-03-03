"""Модуль для Pydantic схем пользователей."""

import uuid

from pydantic import (
    BaseModel,
    Field,
)

from src.schemas import DataListReadBaseSchema, PaginationBaseSchema


# MARK: User
class UserReadSchema(BaseModel):
    """Pydantic схема для получения пользователя."""

    id: uuid.UUID = Field(description="ID пользователя.")
    email: str = Field(description="Электронная почта пользователя.")
    full_name: str = Field(description="Полное имя пользователя.")

    class Config:
        json_encoders = {uuid.UUID: str}
        from_attributes = True


class UserLoginSchema(BaseModel):
    """Pydantic схема для авторизации пользователя."""

    email: str = Field(description="Электронная почта пользователя.")
    password: str = Field(description="Пароль пользователя.")


class UserCreateSchema(BaseModel):
    """Pydantic схема для создания пользователя."""

    email: str = Field(description="Электронная почта пользователя.")
    password: str = Field(description="Пароль пользователя.")
    full_name: str = Field(description="Полное имя пользователя.")


class UserCreateRepositorySchema(BaseModel):
    """Pydantic схема для создания пользователя в БД."""

    email: str = Field(description="Электронная почта пользователя.")
    hashed_password: str = Field(description="Хэшированный пароль пользователя.")
    full_name: str = Field(description="Полное имя пользователя.")


class UserUpdateSchema(BaseModel):
    """Pydantic схема для обновления данных пользователя."""

    email: str | None = Field(
        default=None,
        description="Электронная почта пользователя.",
    )
    password: str | None = Field(
        default=None,
        description="Пароль пользователя.",
    )
    full_name: str | None = Field(
        default=None,
        description="Полное имя пользователя.",
    )


class UserUpdateRepositorySchema(BaseModel):
    """Pydantic схема для обновления данных пользователя в БД."""

    email: str | None = Field(
        default=None,
        description="Электронная почта пользователя.",
    )
    hashed_password: str | None = Field(
        default=None,
        description="Хэшированный пароль пользователя.",
    )
    full_name: str | None = Field(
        default=None,
        description="Полное имя пользователя.",
    )


# MARK: Admin
class UserReadAdminSchema(UserReadSchema):
    """
    Pydantic схема для отображения
    пользователя в запросах администратора.
    """

    is_admin: bool = Field(
        description="Является ли пользователь администратором.",
    )


class UserCreateAdminSchema(UserCreateSchema):
    """Pydantic схема для создания пользователя администратором."""

    is_admin: bool = Field(
        description="Является ли пользователь администратором.",
    )


class UserCreateRepositoryAdminSchema(UserCreateRepositorySchema):
    """Pydantic схема для создания пользователя администратором в БД."""

    is_admin: bool = Field(
        description="Является ли пользователь администратором.",
    )


class UserUpdateAdminSchema(UserUpdateSchema):
    """Pydantic схема для обновления данных пользователя администратором."""

    is_admin: bool = Field(
        description="Является ли пользователь администратором.",
    )


class UserUpdateRepositoryAdminSchema(UserUpdateRepositorySchema):
    """Pydantic схема для обновления данных пользователя администратором в БД."""

    is_admin: bool | None = Field(
        default=None,
        description="Является ли пользователь администратором.",
    )


class UserListReadSchema(DataListReadBaseSchema):
    """Pydantic схема для получения пользователя."""

    users: list[UserReadAdminSchema] = Field(
        description="Список пользователей, соответствующих query параметрам.",
    )


# MARK: Query
class UsersQuerySchema(PaginationBaseSchema):
    """
    Основная схема query параметров для запроса
    списка пользователей от имени администратора.
    """

    id: uuid.UUID | None = Field(
        default=None,
        description="ID пользователя.",
    )
    email: str | None = Field(
        default=None,
        description="Электронная почта пользователя.",
    )
    full_name: str | None = Field(
        default=None,
        description="Полное имя пользователя.",
    )
    is_admin: bool | None = Field(
        default=None,
        description="Является ли пользователь администратором.",
    )
    asc: bool = Field(
        default=False,
        description=(
            "Порядок сортировки пользователей по дате создания. "
            "По умолчанию — от новых к старым."
        ),
    )

    class Config:
        extra = "forbid"
