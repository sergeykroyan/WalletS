"""make account name unique

Revision ID: 4ef56832e611
Revises: 98ddf1d3c802
Create Date: 2025-02-17 18:24:10.637174

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4ef56832e611"
down_revision: Union[str, None] = "98ddf1d3c802"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        op.f("uq_accounts_account_name"), "accounts", ["account_name"]
    )


def downgrade() -> None:
    op.drop_constraint(op.f("uq_accounts_account_name"), "accounts", type_="unique")
