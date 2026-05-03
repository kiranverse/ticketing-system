"""creating user model

Revision ID: 480f72dde8f0
Revises: 9e4a14f43f93
Create Date: 2026-05-03 11:26:50.948526

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '480f72dde8f0'
down_revision: Union[str, Sequence[str], None] = '9e4a14f43f93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
    )

    op.create_index('ix_users_id', 'users', ['id'])

    # Remove old unique constraint (if exists)
    try:
        op.drop_constraint('uq_bookings_seat_id', 'bookings', type_='unique')
    except:
        pass

    # Add foreign key from bookings → users
    op.create_foreign_key(
        'fk_bookings_user_id_users',
        'bookings',
        'users',
        ['user_id'],
        ['id']
    )


def downgrade():
    op.drop_constraint('fk_bookings_user_id_users', 'bookings', type_='foreignkey')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
