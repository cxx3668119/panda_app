"""add bound record id to app user

Revision ID: edb862b69f4f
Revises: b829ca421fdd
Create Date: 2026-05-11 13:33:44.732403

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'edb862b69f4f'
down_revision: Union[str, Sequence[str], None] = 'b829ca421fdd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('app_user', sa.Column('bound_record_id', sa.BigInteger(), nullable=True))
    op.alter_column(
        'user_record',
        'birthday',
        existing_type=sa.Date(),
        type_=sa.DateTime(),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'user_record',
        'birthday',
        existing_type=sa.DateTime(),
        type_=sa.Date(),
        existing_nullable=False,
    )
    op.drop_column('app_user', 'bound_record_id')
