from fastapi import HTTPException, status


# MARK: Base
class BaseConflictException(HTTPException):
    """
    Основной класс исключений в случае конфликта при создании данных.

    Код ответа - `HTTP_409_CONFLICT`.
    """

    default_message = "Возник конфликт при создании данных."

    def __init__(
        self,
        exc: Exception | None = None,
    ):
        status_code = status.HTTP_409_CONFLICT
        if exc:
            self.default_message += f"Exception: {exc}"

        super().__init__(
            status_code=status_code,
            detail=self.default_message,
        )


class BaseNotFoundException(HTTPException):
    """
    Основной класс исключений в случае отсутствия данных.

    Код ответа - `HTTP_404_NOT_FOUND`.
    """

    default_message = "Данные не найдены."

    def __init__(self):
        status_code = status.HTTP_404_NOT_FOUND

        super().__init__(
            status_code=status_code,
            detail=self.default_message,
        )


class BaseBadRequestException(HTTPException):
    """
    Основной класс исключений при некорректном запросе.

    Код ответа - `HTTP_400_BAD_REQUEST`.
    """

    default_message = "Некорректный запрос."

    def __init__(self):
        status_code = status.HTTP_400_BAD_REQUEST

        super().__init__(
            status_code=status_code,
            detail=self.default_message,
        )


class BaseForbiddenException(HTTPException):
    """
    Основной класс исключений при недостаточных
    правах для выполнения запроса.

    Код ответа - `HTTP_400_BAD_REQUEST`.
    """

    default_message = "Недостаточно привилегий для выполнения запроса."

    def __init__(self):
        status_code = status.HTTP_403_FORBIDDEN

        super().__init__(
            status_code=status_code,
            detail=self.default_message,
        )


# MARK: Users
class UserNotFoundException(BaseNotFoundException):
    """Исключение при отсутствии пользователя."""

    default_message = "Пользователь не найден."


class UserConflictException(BaseConflictException):
    """Исключение при попытке создать пользователя."""

    default_message = "Конфликт при создании пользователя."


# MARK: JWT
class TokenExpiredException(HTTPException):
    """Возникает, если время действия токена истекло"""

    def __init__(
        self,
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Время действия токена истекло.",
        )


class InvalidTokenException(HTTPException):
    """Возникает, если передан невалидный токен."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен.",
        )


# MARK: Accounts
class AccountNotFoundException(BaseNotFoundException):
    """Исключение при отсутствии аккаунта."""

    default_message = "Аккаунт не найден."


class AccountConflictException(BaseConflictException):
    """Исключение при попытке создать аккаунт."""

    default_message = "Конфликт при создании аккаунта."


# MARK: Transactions
class TransactionNotFoundException(BaseNotFoundException):
    """Исключение при отсутствии транзакции."""

    default_message = "Транзакция не найдена."


class TransactionConflictException(BaseConflictException):
    """Исключение при попытке создать транзакцию."""

    default_message = "Конфликт при создании транзакции."


class TransactionInvalidSignatureException(BaseBadRequestException):
    """Исключение при некорректной подписи транзакции."""

    default_message = "Некорректная подпись транзакции."
