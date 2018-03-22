from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine
from sqlalchemy_utils import database_exists, create_database

db_url = "mysql+pymysql://root:mariadb@0.0.0.0:3306/justinlab?charset=utf8"

engine = create_engine(db_url)
if not database_exists(engine.url):
    create_database(engine.url)

meta = MetaData(engine)
users = Table("Users", meta,
  Column("id", Integer, primary_key=True),
  Column("name", String(50)),
  Column("idm", String(50)),
  Column("webhook_url", String(2100))
)
meta.create_all()
