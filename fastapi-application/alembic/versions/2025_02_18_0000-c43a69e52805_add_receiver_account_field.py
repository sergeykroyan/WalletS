"""Add receiver account field

Revision ID: c43a69e52805
Revises: ef2ec96cd7cc
Create Date: 2025-02-18 00:00:12.857068

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c43a69e52805"
down_revision: Union[str, None] = "ef2ec96cd7cc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "invoices",
        sa.Column("receiver_account_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        op.f("fk_invoices_receiver_account_id_accounts"),
        "invoices",
        "accounts",
        ["receiver_account_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("fk_invoices_receiver_account_id_accounts"),
        "invoices",
        type_="foreignkey",
    )
    op.drop_column("invoices", "receiver_account_id")
