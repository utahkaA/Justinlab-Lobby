from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine
from sqlalchemy_utils import database_exists, create_database

from models.users import Base, User

def _main():
  db_url = "mysql+pymysql://root:mariadb@0.0.0.0:3306/justinlab?charset=utf8"

  engine = create_engine(db_url)
  if not database_exists(engine.url):
    create_database(engine.url)

  Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
  _main()
