"""add a owner id to the post table

Revision ID: 1d40ccf8ebda
Revises: 586c52081574
Create Date: 2025-05-18 07:11:45.137150

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d40ccf8ebda'
down_revision: Union[str, None] = '586c52081574'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key("post_user_fk", 'posts',referent_table='all_users',local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk',table_name='posts')
    op.drop_column('posts',column_name='owner_id')
    pass
