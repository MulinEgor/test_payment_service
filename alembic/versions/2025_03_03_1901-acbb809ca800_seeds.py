"""seeds

Revision ID: acbb809ca800
Revises: b1ea3d195bc7
Create Date: 2025-03-03 19:01:42.558801+00:00

"""

import uuid
from typing import Sequence, Union

from alembic import op
from src.settings import settings
from src.utils import get_hash

# revision identifiers, used by Alembic.
revision: str = "acbb809ca800"
down_revision: Union[str, None] = "b1ea3d195bc7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создаем обычного пользователя
    if settings.MODE == "DEV":
        user_id = uuid.uuid4()
        op.execute(
            f"""
            INSERT INTO users (id, email, hashed_password, full_name, is_admin)
            VALUES (
                '{user_id}',
                'user@example.com', 
                '{get_hash("user123")}', 
                'Test User', 
                '{False}'
            )
            """
        )

        # Создаем администратора
        admin_id = uuid.uuid4()
        op.execute(
            f"""
            INSERT INTO users (id, email, hashed_password, full_name, is_admin)
            VALUES (
                '{admin_id}',
                'admin@example.com',
                '{get_hash("admin123")}',
                'Test Admin',
                '{True}'
            )
            """
        )

        # Создаем аккаунт для обычного пользователя
        op.execute(
            f"""
            INSERT INTO accounts (id, user_id, balance)
            VALUES (
                '{uuid.uuid4()}',
                '{user_id}',
                1000
            )
            """
        )


def downgrade() -> None:
    # Удаляем созданные данные в режиме разработки
    if settings.MODE == "DEV":
        op.get_bind().execute("DELETE FROM accounts")
        op.get_bind().execute("DELETE FROM users")
