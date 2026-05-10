"""create user record table

Revision ID: b829ca421fdd
Revises: bf63e99af896
Create Date: 2026-05-10 13:31:28.555794

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b829ca421fdd'
down_revision: Union[str, Sequence[str], None] = 'bf63e99af896'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'user_record',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(length=64), nullable=False),
        sa.Column('birthday', sa.DateTime(), nullable=False),
        sa.Column('gender', sa.String(length=16), nullable=False),
        sa.Column('birthplace', sa.String(length=255), nullable=True),
        sa.Column('age', sa.Integer(), nullable=False),
        sa.Column('zodiac', sa.String(length=16), nullable=False),
        sa.Column('horoscope', sa.String(length=16), nullable=False),
        sa.Column('birth_zodiac_sign', sa.String(length=16), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_user_record_user_id', 'user_record', ['user_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_user_record_user_id', table_name='user_record')
    op.drop_table('user_record')
