"""Initial migration

Revision ID: 1de6cbc49648
Revises: 
Create Date: 2026-06-30 23:15:06.334659

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1de6cbc49648'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('allergene',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('auth',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('login', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ingredient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('restaurant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(), nullable=True),
    sa.Column('categorie', sa.String(), nullable=True),
    sa.Column('auth_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['auth_id'], ['auth.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('plat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nom', sa.String(), nullable=True),
    sa.Column('categorie', sa.String(), nullable=True),
    sa.Column('id_restaurant', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_restaurant'], ['restaurant.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('allergeneingredient',
    sa.Column('id_allergene', sa.Integer(), nullable=False),
    sa.Column('id_ingredient', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['id_allergene'], ['allergene.id'], ),
    sa.ForeignKeyConstraint(['id_ingredient'], ['ingredient.id'], ),
    sa.PrimaryKeyConstraint('id_allergene', 'id_ingredient')
    )
    op.create_table('platingredient',
    sa.Column('id_plat', sa.Integer(), nullable=False),
    sa.Column('id_ingredient', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_ingredient'], ['ingredient.id'], ),
    sa.ForeignKeyConstraint(['id_plat'], ['plat.id'], ),
    sa.PrimaryKeyConstraint('id_plat', 'id_ingredient')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('platingredient')
    op.drop_table('allergeneingredient')
    op.drop_table('plat')
    op.drop_table('restaurant')
    op.drop_table('ingredient')
    op.drop_table('auth')
    op.drop_table('allergene')
