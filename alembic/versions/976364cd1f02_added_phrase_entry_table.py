"""added phrase-entry table

Revision ID: 976364cd1f02
Revises: 015b93ddc5db
Create Date: 2023-08-20 17:05:34.051974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '976364cd1f02'
down_revision: Union[str, None] = '015b93ddc5db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'entry_phrase',
        sa.Column('entry_id', sa.Integer(), sa.ForeignKey('entry.id'), nullable=False),
        sa.Column('phrase_id', sa.Integer(), sa.ForeignKey('phrases.id'), nullable=False),
        sa.PrimaryKeyConstraint('entry_id', 'phrase_id')
    )


def downgrade() -> None:
    op.drop_table('entry_phrase')
