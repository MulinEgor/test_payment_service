"""add_users_table

Revision ID: 95620b3452e7
Revises:
Create Date: 2025-03-03 09:07:29.335133+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "95620b3452e7"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.Uuid(),
            nullable=False,
            comment="Уникальный идентификатор пользователя.",
        ),
        sa.Column(
            "email",
            sa.String(),
            nullable=False,
            comment="Электронная почта пользователя.",
        ),
        sa.Column(
            "hashed_password",
            sa.String(),
            nullable=False,
            comment="Хэшированный пароль пользователя.",
        ),
        sa.Column(
            "full_name", sa.String(), nullable=False, comment="Полное имя пользователя."
        ),
        sa.Column(
            "is_admin",
            sa.Boolean(),
            nullable=False,
            comment="Является ли пользователь администратором.",
        ),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP AT TIME ZONE 'UTC')"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("(CURRENT_TIMESTAMP AT TIME ZONE 'UTC')"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("users_pkey")),
        sa.UniqueConstraint("email", name=op.f("users_email_key")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    # ### end Alembic commands ###
