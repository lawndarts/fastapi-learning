"""create posts table

Revision ID: 41643827b7a3
Revises: 
Create Date: 2022-12-15 22:09:31.993423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41643827b7a3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String,nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass