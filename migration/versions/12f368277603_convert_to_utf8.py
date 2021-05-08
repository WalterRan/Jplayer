"""convert to utf8

Revision ID: 12f368277603
Revises: 6dbc11710211
Create Date: 2021-05-08 07:19:50.985734

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12f368277603'
down_revision = '6dbc11710211'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    conn.execute(sa.sql.text('ALTER table media_list CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci'))


def downgrade():
    conn = op.get_bind()

    conn.execute(sa.sql.text('ALTER table media_list CONVERT TO CHARACTER SET latin1 COLLATE latin1_swedish_ci'))

