"""Add account name and number

Revision ID: 98ddf1d3c802
Revises: bfb8b33a1ff5
Create Date: 2025-02-17 17:26:22.475691

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "98ddf1d3c802"
down_revision: Union[str, None] = "bfb8b33a1ff5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "accounts",
        sa.Column("account_name", sa.String(length=100), nullable=False),
    )
    op.add_column(
        "accounts",
        sa.Column("account_number", sa.String(length=12), nullable=False),
    )
    op.create_index(
        op.f("ix_accounts_account_number"),
        "accounts",
        ["account_number"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_accounts_account_number"), table_name="accounts")
    op.drop_column("accounts", "account_number")
    op.drop_column("accounts", "account_name")
