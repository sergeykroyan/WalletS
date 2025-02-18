"""remove account name uniqueness

Revision ID: c9c070dd1266
Revises: c43a69e52805
Create Date: 2025-02-18 16:11:55.908058

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c9c070dd1266"
down_revision: Union[str, None] = "c43a69e52805"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("uq_accounts_account_name", "accounts", type_="unique")


def downgrade() -> None:
    op.create_unique_constraint(
        "uq_accounts_account_name", "accounts", ["account_name"]
    )
