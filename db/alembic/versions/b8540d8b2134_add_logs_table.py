"""add logs table

Revision ID: b8540d8b2134
Revises: f959b54b7d36
Create Date: 2018-03-29 17:06:30.415057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8540d8b2134'
down_revision = 'f959b54b7d36'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
    'logs',
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("stuid", sa.String(7), sa.ForeignKey("users.stuid"), nullable=False),
    sa.Column("timestamp", sa.Integer, nullable=False),
    sa.Column("status", sa.String(6), nullable=False),
    sa.Column("is_touched", sa.Boolean, nullable=False),
  )

def downgrade():
  op.drop_table('logs')
