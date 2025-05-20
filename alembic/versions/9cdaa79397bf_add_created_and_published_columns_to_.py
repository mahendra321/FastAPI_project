"""add created and published columns to posts

Revision ID: 9cdaa79397bf
Revises: 1d40ccf8ebda
Create Date: 2025-05-18 07:47:36.729205

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9cdaa79397bf'
down_revision: Union[str, None] = '1d40ccf8ebda'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'))
    op.add_column('posts',
                  sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts','created_at')
    op.drop_column('posts','published')
    pass
