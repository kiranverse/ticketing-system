"""add unique constraint on seat_id in bookings

Revision ID: 9e4a14f43f93
Revises: 49460d598bc8
Create Date: 2026-04-30 18:24:42.285403

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e4a14f43f93'
down_revision: Union[str, Sequence[str], None] = '49460d598bc8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint('uq_bookings_seat_id', 'bookings', ['seat_id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('uq_bookings_seat_id', 'bookings', type_='unique')
