"""init

Revision ID: 0cba15d1c00b
Revises: 
Create Date: 2018-03-24 21:32:24.372146

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0cba15d1c00b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
    'users',
    sa.Column('stuid', sa.String(7), primary_key=True, nullable=False),
    sa.Column('name', sa.String(50), nullable=False),
    sa.Column('webhook', sa.String(2100), nullable=False),
    sa.Column('created_at', sa.BigInteger, nullable=False),
    sa.Column('updated_at', sa.BigInteger, nullable=False),
  )


def downgrade():
  op.drop_table('users')
