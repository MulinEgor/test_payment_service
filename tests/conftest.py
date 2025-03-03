"""Основной модуль `conftest` для всех тестов."""

import asyncio
import sys
import uuid
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from faker import Faker
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

import src.accounts.schemas as account_schemas
import src.auth.schemas as auth_schemas
import src.transactions.schemas as transaction_schemas
import src.users.schemas as user_schemas
from src import utils
from src.accounts.models import AccountModel
from src.auth.services import JWTService
from src.settings import settings
from src.transactions.models.transaction_model import TransactionModel
from src.users.models import UserModel

faker = Faker()


# MARK: DBSession
@pytest_asyncio.fixture(scope="module")
async def engine(request, worker_id) -> AsyncGenerator[AsyncEngine, None]:
    """
    Создает экземпляр `AsyncEngine' с URL-адресом базы данных,
    соответствующим процессу pytest.

    Область действия `module` задается, поскольку каждый модуль c тестами
    выполняется в отдельном процессе pytest, чтобы гарантировать, что
    он подключается к соответствующей базе данных.
    """

    engine = create_async_engine(
        url=(
            f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
            f"{settings.POSTGRES_HOST}-{worker_id}:{settings.POSTGRES_PORT}/{worker_id}"
        ),
        poolclass=NullPool,
    )

    yield engine


@pytest.fixture(scope="function")
async def session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """
    Создать соединение с Postgres, начать транзакцию,
    а затем привязать это соединение к сессии с вложенной транзакцией.

    Вложенная транзакция обеспечивает изоляцию внутри тестов, позволяя
    фиксировать изменения во внутренней транзакции так, чтобы они были
    видны только для тестов, где она используется, но не фиксировать их
    в БД полностью, поскольку коммит внешней транзакции
    никогда не будет выполнен.

    Параметр `scope="function"` обеспечивает запуск этой фикстуры перед запуском каждого
    теста. Так что после запуска каждого теста, данные в БД откатываются.
    Каждый тест работает изолированно от других.

    Используется движок, соответствующий процессу `pytest`.
    """

    AsyncSession = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    async with engine.connect() as conn:
        tsx = await conn.begin()
        async with AsyncSession(bind=conn) as session:
            nested_tsx = await conn.begin_nested()

            yield session

            if nested_tsx.is_active:
                await nested_tsx.rollback()
            await tsx.rollback()


@pytest.fixture()
async def task_session(
    session: AsyncSession,
    mocker,
) -> AsyncSession:
    """Мокирование сессии для выполнения задач Celery."""

    async def mock_get_session():
        yield session

    mocker.patch("tasks.db_session.get_session", return_value=mock_get_session())
    return session


# MARK: Loop
@pytest.fixture(scope="session")
def event_loop(request):
    """
    Фикстура для создания и закрытия event loop.
    """

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# MARK: Output
@pytest.fixture(autouse=True, scope="session")
def output_to_stdout():
    """
    Перенаправить `stdout` в `stderr`,
    для вывода логов при отладки в `pytest-xdist`.
    """

    sys.stdout = sys.stderr


# MARK: Users
@pytest_asyncio.fixture
async def user_db(session: AsyncSession) -> UserModel:
    """Добавить пользователя в БД."""

    user_db = UserModel(
        id=str(uuid.uuid4()),
        email=faker.email(),
        hashed_password=utils.get_hash(faker.password()),
        full_name=faker.name(),
    )
    session.add(user_db)
    await session.commit()

    return user_db


@pytest_asyncio.fixture
async def user_admin_db(session: AsyncSession) -> UserModel:
    """Добавить пользователя-администратора в БД."""

    user_admin = UserModel(
        id=str(uuid.uuid4()),
        email=faker.email(),
        hashed_password=utils.get_hash(faker.password()),
        full_name=faker.name(),
        is_admin=True,
    )
    session.add(user_admin)
    await session.commit()

    return user_admin


@pytest_asyncio.fixture
async def user_create_data() -> user_schemas.UserReadAdminSchema:
    """
    Подготовленные данные для создания
    пользователя в БД администратором.
    """

    return user_schemas.UserCreateAdminSchema(
        email=faker.email(),
        password=faker.password(),
        full_name=faker.name(),
        is_admin=False,
    )


@pytest_asyncio.fixture
async def user_update_data() -> user_schemas.UserUpdateAdminSchema:
    """
    Подготовленные данные для обновления
    пользователя в БД администратором.
    """

    return user_schemas.UserUpdateAdminSchema(
        email=faker.email(),
        password=faker.password(),
        full_name=faker.name(),
        is_admin=True,
    )


# MARK: JWT
@pytest_asyncio.fixture
async def user_jwt_tokens(user_db: UserModel) -> auth_schemas.JWTGetSchema:
    """Создать JWT токены  для тестового пользователя."""

    return await JWTService.create_tokens(user_id=user_db.id)


@pytest_asyncio.fixture
async def admin_jwt_tokens(user_admin_db: UserModel) -> auth_schemas.JWTGetSchema:
    """Создать JWT токены  для тестового пользователя-администратора."""

    return await JWTService.create_tokens(user_id=user_admin_db.id)


# MARK: Accounts
@pytest_asyncio.fixture
async def account_db(
    session: AsyncSession,
    user_db: UserModel,
) -> AccountModel:
    """Добавить аккаунт в БД."""

    account_db = AccountModel(
        user_id=user_db.id,
    )
    session.add(account_db)
    await session.commit()

    return account_db


@pytest_asyncio.fixture
async def account_create_data() -> account_schemas.AccountCreateSchema:
    """Подготовленные данные для создания аккаунта в БД."""

    return account_schemas.AccountCreateSchema(
        balance=0,
        user_id=user_db.id,
    )


# MARK: Transactions
@pytest_asyncio.fixture
async def transaction_db(
    session: AsyncSession,
    account_db: AccountModel,
    user_db: UserModel,
) -> TransactionModel:
    """Добавить транзакцию в БД."""

    transaction_db = TransactionModel(
        id=str(uuid.uuid4()),
        account_id=account_db.id,
        amount=faker.random_int(),
        user_id=user_db.id,
        signature=faker.password(),
    )
    session.add(transaction_db)
    await session.commit()

    return transaction_db


@pytest_asyncio.fixture
async def transaction_create_data(
    user_db: UserModel,
    account_db: AccountModel,
) -> transaction_schemas.TransactionSchema:
    """Подготовленные данные для создания транзакции в БД."""

    id, account_id, user_id, amount = (
        str(faker.random_int()),
        str(account_db.id),
        str(user_db.id),
        faker.random_int(),
    )
    signature = utils.get_hash(
        account_id + str(amount) + id + user_id + settings.TRANSACTION_SIGNATURE_SECRET
    )

    return transaction_schemas.TransactionSchema(
        id=id,
        account_id=account_id,
        amount=amount,
        user_id=user_id,
        signature=signature,
    )
