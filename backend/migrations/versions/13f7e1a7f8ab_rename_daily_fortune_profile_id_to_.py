"""rename daily fortune profile_id to record_id

Revision ID: 13f7e1a7f8ab
Revises: 102292082735
Create Date: 2026-05-11 21:33:13.461824

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '13f7e1a7f8ab'
down_revision: Union[str, Sequence[str], None] = '102292082735'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(op.f('fk_daily_fortune_profile'), 'daily_fortune', type_='foreignkey')
    op.drop_constraint(op.f('uk_daily_fortune'), 'daily_fortune', type_='unique')
    op.drop_index(op.f('idx_daily_fortune_profile_date'), table_name='daily_fortune')
    op.alter_column(
        'daily_fortune',
        'profile_id',
        new_column_name='record_id',
        existing_type=mysql.BIGINT(),
        existing_nullable=False,
    )
    op.create_index('idx_daily_fortune_record_date', 'daily_fortune', ['record_id', 'fortune_date'], unique=False)
    op.create_unique_constraint('uk_daily_fortune', 'daily_fortune', ['user_id', 'record_id', 'fortune_date'])
    op.create_foreign_key('fk_daily_fortune_record', 'daily_fortune', 'user_record', ['record_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_daily_fortune_record', 'daily_fortune', type_='foreignkey')
    op.drop_constraint('uk_daily_fortune', 'daily_fortune', type_='unique')
    op.drop_index('idx_daily_fortune_record_date', table_name='daily_fortune')
    op.alter_column(
        'daily_fortune',
        'record_id',
        new_column_name='profile_id',
        existing_type=mysql.BIGINT(),
        existing_nullable=False,
    )
    op.create_index(op.f('idx_daily_fortune_profile_date'), 'daily_fortune', ['profile_id', 'fortune_date'], unique=False)
    op.create_unique_constraint(op.f('uk_daily_fortune'), 'daily_fortune', ['user_id', 'profile_id', 'fortune_date'])
    op.create_foreign_key(op.f('fk_daily_fortune_profile'), 'daily_fortune', 'bazi_profile', ['profile_id'], ['id'])
