"""create cards

Revision ID: f959b54b7d36
Revises: 0cba15d1c00b
Create Date: 2018-03-24 21:50:59.476088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f959b54b7d36'
down_revision = '0cba15d1c00b'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
    'cards',
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("stuid", sa.String(7), sa.ForeignKey("users.stuid"), nullable=False),
    sa.Column("idm", sa.String(64), nullable=False),
    sa.Column("pmm", sa.String(64), nullable=False),
    sa.Column("sys", sa.String(64), nullable=False),
    sa.Column('created_at', sa.Integer, nullable=False),
    sa.Column('updated_at', sa.Integer, nullable=False),
  )


def downgrade():
  op.drop_table('cards')
