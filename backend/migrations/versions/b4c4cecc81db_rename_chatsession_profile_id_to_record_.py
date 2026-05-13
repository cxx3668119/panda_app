"""rename chatsession profile_id to record_id

Revision ID: b4c4cecc81db
Revises: 13f7e1a7f8ab
Create Date: 2026-05-13 21:05:54.382138

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'b4c4cecc81db'
down_revision: Union[str, Sequence[str], None] = '13f7e1a7f8ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint('fk_ai_chat_session_profile', 'ai_chat_session', type_='foreignkey')
    op.drop_index('idx_ai_chat_session_profile_date', table_name='ai_chat_session')
    op.alter_column(
        'ai_chat_session',
        'profile_id',
        new_column_name='record_id',
        existing_type=mysql.BIGINT(),
        existing_nullable=False,
    )
    op.create_index('idx_ai_chat_session_record_date', 'ai_chat_session', ['record_id', 'session_date'], unique=False)
    op.create_foreign_key('fk_ai_chat_session_record', 'ai_chat_session', 'user_record', ['record_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('fk_ai_chat_session_record', 'ai_chat_session', type_='foreignkey')
    op.drop_index('idx_ai_chat_session_record_date', table_name='ai_chat_session')
    op.alter_column(
        'ai_chat_session',
        'record_id',
        new_column_name='profile_id',
        existing_type=mysql.BIGINT(),
        existing_nullable=False,
    )
    op.create_index('idx_ai_chat_session_profile_date', 'ai_chat_session', ['profile_id', 'session_date'], unique=False)
    op.create_foreign_key('fk_ai_chat_session_profile', 'ai_chat_session', 'bazi_profile', ['profile_id'], ['id'])
