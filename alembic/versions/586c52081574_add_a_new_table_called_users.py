"""add a new table called users

Revision ID: 586c52081574
Revises: 73e4acc0a7e8
Create Date: 2025-05-18 06:17:04.954120

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '586c52081574'
down_revision: Union[str, None] = '73e4acc0a7e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('all_users',
                  sa.Column('id',sa.Integer(),nullable=False),
                  sa.Column('email', sa.String(), nullable=False),
                  sa.Column('password', sa.String(), nullable= False),
                  sa.Column('created at', sa.TIMESTAMP(timezone=True),
                            server_default=sa.text('now()'),  nullable=False),
                  sa.PrimaryKeyConstraint('id'),
                  sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table('Users')
    pass
