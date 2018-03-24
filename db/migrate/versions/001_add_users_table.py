from sqlalchemy import *
from migrate import *
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, DATETIME, TEXT

meta = MetaData()
table = Table(
  'users', meta,
  Column('id', BIGINT(unsigned=True), primary_key=True),
  Column('stuid', VARCHAR(7), nullable=False),
  Column('name', VARCHAR(50), nullable=False),
  Column('webhook', VARCHAR(2100), nullable=False),
  Column('created_at', DATETIME, nullable=False),
  Column('updated_at', DATETIME, nullable=False))

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    table.create()

def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    table.drop()
