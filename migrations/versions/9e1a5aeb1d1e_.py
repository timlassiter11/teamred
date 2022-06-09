"""Add airport table

Revision ID: 9e1a5aeb1d1e
Revises: d8a41be3e4c9
Create Date: 2022-05-30 09:13:35.996690

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e1a5aeb1d1e'
down_revision = 'd8a41be3e4c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('airport',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=3), nullable=True),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('timezone', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_airport_code'), 'airport', ['code'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_airport_code'), table_name='airport')
    op.drop_table('airport')
    # ### end Alembic commands ###
