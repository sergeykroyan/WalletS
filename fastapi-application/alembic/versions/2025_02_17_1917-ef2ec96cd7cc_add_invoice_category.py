from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ef2ec96cd7cc"
down_revision: Union[str, None] = "4ef56832e611"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


invoice_category_enum = sa.Enum(
    "deposit",
    "withdrawal",
    "internal_transfer",
    "external_transfer",
    name="invoicecategory",
)


def upgrade() -> None:
    invoice_category_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "invoices",
        sa.Column(
            "category", invoice_category_enum, nullable=False, server_default="deposit"
        ),
    )


def downgrade() -> None:
    op.drop_column("invoices", "category")

    invoice_category_enum.drop(op.get_bind(), checkfirst=True)
