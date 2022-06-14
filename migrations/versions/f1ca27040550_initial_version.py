"""initial version

Revision ID: f1ca27040550
Revises: 
Create Date: 2022-06-14 15:59:26.257736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1ca27040550'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('airport',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=3), nullable=True),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('timezone', sa.String(length=120), nullable=False),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('state', sa.String(length=120), nullable=True),
    sa.Column('latitude', sa.Integer(), nullable=False),
    sa.Column('longitude', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_airport_code'), 'airport', ['code'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('first_name', sa.String(length=120), nullable=True),
    sa.Column('last_name', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('role', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('airplane',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('registration_number', sa.String(length=120), nullable=True),
    sa.Column('model_name', sa.String(length=120), nullable=False),
    sa.Column('model_code', sa.String(length=120), nullable=False),
    sa.Column('capacity', sa.Integer(), nullable=False),
    sa.Column('range', sa.Integer(), nullable=False),
    sa.Column('home_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['home_id'], ['airport.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_airplane_registration_number'), 'airplane', ['registration_number'], unique=True)
    op.create_table('flight',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.String(length=4), nullable=True),
    sa.Column('airplane_id', sa.Integer(), nullable=True),
    sa.Column('departing_id', sa.Integer(), nullable=True),
    sa.Column('arriving_id', sa.Integer(), nullable=True),
    sa.Column('departure_time', sa.Time(), nullable=False),
    sa.Column('arrival_time', sa.Time(), nullable=False),
    sa.Column('cost', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['airplane_id'], ['airplane.id'], ),
    sa.ForeignKeyConstraint(['arriving_id'], ['airport.id'], ),
    sa.ForeignKeyConstraint(['departing_id'], ['airport.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_flight_number'), 'flight', ['number'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_flight_number'), table_name='flight')
    op.drop_table('flight')
    op.drop_index(op.f('ix_airplane_registration_number'), table_name='airplane')
    op.drop_table('airplane')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_airport_code'), table_name='airport')
    op.drop_table('airport')
    # ### end Alembic commands ###
