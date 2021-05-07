"""media_list

Revision ID: 6dbc11710211
Revises: 
Create Date: 2021-05-07 11:52:44.055429

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6dbc11710211'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'media_list',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, primary_key=True),
        sa.Column('name', sa.String(255), nullable=True),
        sa.Column('path', sa.String(255), nullable=False),
        sa.Column('priority', sa.Integer(), nullable=False),
        sa.Column('played', sa.Integer(), nullable=False),
        sa.Column('failed', sa.Integer(), nullable=False),
        sa.Column('jumped', sa.Integer(), nullable=False))

def downgrade():
    op.drop_table('media_list')

