"""add user table

Revision ID: 059caf2325fb
Revises: b3b30530b196
Create Date: 2022-12-15 22:33:49.423093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '059caf2325fb'
down_revision = 'b3b30530b196'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    #different way of setting constraints
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
