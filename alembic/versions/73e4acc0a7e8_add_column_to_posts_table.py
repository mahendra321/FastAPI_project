"""add column to posts table

Revision ID: 73e4acc0a7e8
Revises: fb755ad7ca10
Create Date: 2025-05-18 05:48:23.074373

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73e4acc0a7e8'
down_revision: Union[str, None] = 'fb755ad7ca10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts',
                   'content')
    pass
