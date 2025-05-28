"""Add user, floor table and update inventory/collection_log

Revision ID: ea7f7b11766d
Revises: afedee811b2a
Create Date: 2025-05-27 22:21:40.705040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea7f7b11766d'
down_revision = 'afedee811b2a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add 'user' table
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.Text(), nullable=False)
    )

    # Update 'inventory' table: add user_id and foreign key
    op.add_column('inventory', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_inventory_user', 'inventory', 'user', ['user_id'], ['id'])

    # Update 'collection_log': add user_id and make quantity_collected an Integer
    op.add_column('collection_log', sa.Column('user_id', sa.Integer(), nullable=False))
    op.execute("""
    ALTER TABLE collection_log
    ALTER COLUMN quantity_collected
    TYPE INTEGER USING quantity_collected::integer
""")
    op.create_foreign_key('fk_collection_log_user', 'collection_log', 'user', ['user_id'], ['id'])

    # Add 'floor' table
    op.create_table(
        'floor',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('item_sku', sa.Text(), sa.ForeignKey('item.sku'), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('dropped_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False)
    )


def downgrade() -> None:
    # Drop 'floor' table
    op.drop_table('floor')

    # Remove user_id and constraints from 'collection_log'
    op.drop_constraint('fk_collection_log_user', 'collection_log', type_='foreignkey')
    op.drop_column('collection_log', 'user_id')
    op.alter_column('collection_log', 'quantity_collected', type_=sa.Text())

    # Remove user_id and constraints from 'inventory'
    op.drop_constraint('fk_inventory_user', 'inventory', type_='foreignkey')
    op.drop_column('inventory', 'user_id')

    # Drop 'user' table
    op.drop_table('user')