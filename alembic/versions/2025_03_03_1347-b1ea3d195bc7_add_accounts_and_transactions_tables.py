"""add_accounts_and_transactions_tables

Revision ID: b1ea3d195bc7
Revises: 95620b3452e7
Create Date: 2025-03-03 13:47:19.966922+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b1ea3d195bc7"
down_revision: Union[str, None] = "95620b3452e7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "accounts",
        sa.Column("id", sa.UUID(), nullable=False, comment="Идентификатор аккаунта."),
        sa.Column("balance", sa.Integer(), nullable=False, comment="Баланс аккаунта."),
        sa.Column(
            "user_id", sa.UUID(), nullable=False, comment="Идентификатор пользователя."
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("accounts_user_id_fkey")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("accounts_pkey")),
    )
    op.create_table(
        "transactions",
        sa.Column(
            "id", sa.String(), nullable=False, comment="Идентификатор транзакции."
        ),
        sa.Column(
            "account_id", sa.UUID(), nullable=False, comment="Идентификатор аккаунта."
        ),
        sa.Column(
            "user_id", sa.UUID(), nullable=False, comment="Идентификатор пользователя."
        ),
        sa.Column("amount", sa.Integer(), nullable=False, comment="Сумма транзакции."),
        sa.Column(
            "signature", sa.String(), nullable=False, comment="Подпись транзакции."
        ),
        sa.ForeignKeyConstraint(
            ["account_id"], ["accounts.id"], name=op.f("transactions_account_id_fkey")
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("transactions_user_id_fkey")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("transactions_pkey")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("transactions")
    op.drop_table("accounts")
    # ### end Alembic commands ###
