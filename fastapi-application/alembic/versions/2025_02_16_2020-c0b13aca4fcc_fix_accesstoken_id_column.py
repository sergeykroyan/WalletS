"""Fix AccessToken id column

Revision ID: c0b13aca4fcc
Revises: 5792ccf179fb
Create Date: 2025-02-16 20:20:48.956048

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c0b13aca4fcc"
down_revision: Union[str, None] = "5792ccf179fb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("access_tokens", "id")


def downgrade() -> None:
    op.add_column(
        "access_tokens",
        sa.Column("id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
