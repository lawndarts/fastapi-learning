"""add content to posts table

Revision ID: b3b30530b196
Revises: 41643827b7a3
Create Date: 2022-12-15 22:27:02.896643

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3b30530b196'
down_revision = '41643827b7a3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
