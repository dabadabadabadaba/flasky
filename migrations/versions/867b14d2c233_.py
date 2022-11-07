"""empty message

Revision ID: 867b14d2c233
Revises: 9946c4082d1d
Create Date: 2022-11-07 11:17:29.793329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '867b14d2c233'
down_revision = '9946c4082d1d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menu',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('restaurant_name', sa.String(), nullable=True),
    sa.Column('meal', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('breakfast', sa.Column('menu_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'breakfast', 'menu', ['menu_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'breakfast', type_='foreignkey')
    op.drop_column('breakfast', 'menu_id')
    op.drop_table('menu')
    # ### end Alembic commands ###
