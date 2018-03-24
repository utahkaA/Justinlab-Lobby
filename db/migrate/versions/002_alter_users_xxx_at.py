from sqlalchemy import *
from migrate import *
from sqlalchemy.dialects.mysql import BIGINT, DATETIME


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta = MetaData(bind=migrate_engine)
    users = Table("users", meta, autoload=True)
    users.c.created_at.alter(type=BIGINT(13))
    users.c.updated_at.alter(type=BIGINT(13))


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta = MetaData(bind=migrate_engine)
    users = Table("users", meta, autoload=True)
    users.c.created_at.alter(type=DATETIME)
    users.c.updated_at.alter(type=DATETIME)
