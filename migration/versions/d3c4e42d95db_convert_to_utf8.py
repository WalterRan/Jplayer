"""convert to utf8

Revision ID: d3c4e42d95db
Revises: 29f08bd14ca2
Create Date: 2021-05-08 11:42:24.675251

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3c4e42d95db'
down_revision = '29f08bd14ca2'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    conn.execute(sa.sql.text('ALTER table media_list CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci'))


def downgrade():
    conn = op.get_bind()

    conn.execute(sa.sql.text('ALTER table media_list CONVERT TO CHARACTER SET latin1 COLLATE latin1_swedish_ci'))

