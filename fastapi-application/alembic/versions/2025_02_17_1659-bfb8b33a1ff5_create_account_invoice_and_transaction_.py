"""Create account, invoice and transaction tables

Revision ID: bfb8b33a1ff5
Revises: c0b13aca4fcc
Create Date: 2025-02-17 16:59:58.603315

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bfb8b33a1ff5"
down_revision: Union[str, None] = "c0b13aca4fcc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "accounts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("balance", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_accounts_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_accounts")),
    )
    op.create_table(
        "invoices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column(
            "status",
            sa.Enum("pending", "approved", "declined", name="invoicestatus"),
            nullable=False,
        ),
        sa.Column("reviewed_by", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["accounts.id"],
            name=op.f("fk_invoices_account_id_accounts"),
        ),
        sa.ForeignKeyConstraint(
            ["reviewed_by"],
            ["users.id"],
            name=op.f("fk_invoices_reviewed_by_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_invoices")),
    )
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sender_account_id", sa.Integer(), nullable=True),
        sa.Column("receiver_account_id", sa.Integer(), nullable=True),
        sa.Column("invoice_id", sa.Integer(), nullable=True),
        sa.Column("amount", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum(
                "initiated",
                "processing",
                "completed",
                "failed",
                name="transactionstatus",
            ),
            nullable=False,
        ),
        sa.Column(
            "category",
            sa.Enum("deposit", "transfer", "withdrawal", name="transactioncategory"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["invoice_id"],
            ["invoices.id"],
            name=op.f("fk_transactions_invoice_id_invoices"),
        ),
        sa.ForeignKeyConstraint(
            ["receiver_account_id"],
            ["accounts.id"],
            name=op.f("fk_transactions_receiver_account_id_accounts"),
        ),
        sa.ForeignKeyConstraint(
            ["sender_account_id"],
            ["accounts.id"],
            name=op.f("fk_transactions_sender_account_id_accounts"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_transactions")),
    )


def downgrade() -> None:
    op.drop_table("transactions")
    op.drop_table("invoices")
    op.drop_table("accounts")
