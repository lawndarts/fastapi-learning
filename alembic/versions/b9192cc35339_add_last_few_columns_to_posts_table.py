"""add last few columns to posts table

Revision ID: b9192cc35339
Revises: c0862ac5ec68
Create Date: 2022-12-15 23:45:04.784491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9192cc35339'
down_revision = 'c0862ac5ec68'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published',sa.Boolean, server_default = 'TRUE', nullable = False))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default = sa.text('now()'), nullable = False))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
