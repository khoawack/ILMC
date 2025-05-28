"""adding drop rates table

Revision ID: bcc873783ce0
Revises: ea7f7b11766d
Create Date: 2025-05-28 05:35:51.090505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcc873783ce0'
down_revision = 'ea7f7b11766d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
    "drop_rates",
    sa.Column("id", sa.Integer, primary_key=True, index=True),
    sa.Column("pickaxe_sku", sa.Text, sa.ForeignKey("item.sku"), nullable=False),
    sa.Column("item_sku", sa.Text, sa.ForeignKey("item.sku"), nullable=False),
    sa.Column("drop_chance", sa.Float, nullable=False),
)


def downgrade() -> None:
    op.drop_table("drop_rates")
