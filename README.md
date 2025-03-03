# FastAPI Auth Template

[![Static Badge](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org)
[![Static Badge](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Static Badge](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)](https://swagger.io)
[![Static Badge](https://img.shields.io/badge/postgresql-4169e1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Static Badge](https://img.shields.io/badge/-SQLAlchemy-ffd54?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Static Badge](https://img.shields.io/badge/docker-257bd6?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)


## Настройка и запуск проекта

1. Установите [uv](https://docs.astral.sh/uv/getting-started/installation/).

2. Установите зависимости, включая dev:

```bash
uv sync --extra dev
```

3. Создайте `.env` на основе `.env.example`:

```bash
cp -r src/.env.example src/.env
```

4. Запустите проект:

    - С помощью docker-compose:
    ```bash
    make start_dev // Запуск в режиме разработки
    make migrate // Применение миграций
    ```

    - С помощью uvicorn:
    ```bash
    uvicorn src.main:app --reload // Запуск в режиме разработки
    alembic upgrade head // Применение миграций
    ```

## Тестовые данные (можно посмотреть в последней миграции alembic)

Данные для обычного пользователя:
```bash
email: user@example.com
password: user123
```

Данные для администратора:
```bash
email: admin@example.com
password: admin123
```

## Документация

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc


## Тесты
1. Перед началом тестирования, вам нужно создать `.env.test` на основе `.env.test.example`:
```bash
cp -r src/.env.test.example src/.env.test
```

2. По умолчанию, тесты запускаются на 2 контейнерах PostgreSQL.

3. После завершения тестирования, в `htmlcov/index.html` вы можете увидеть покрытие тестов.

