from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class User(Base):
  __tablename__ = "users"
  id = Column("id", Integer, primary_key=True)
  name = Column("name", String(50))
  idm = Column("idm", String(50))
  webhook_url = Column("webhook_url", String(2100))

def _main():
  db_url = "mysql+pymysql://root:mariadb@0.0.0.0:3306/justinlab?charset=utf8"
  engine = create_engine(db_url)
  session = scoped_session(
    sessionmaker(
      autocommit = False,
      autoflush = False,
      bind=engine
    )
  )

  user = User()
  user.name = "utahka"
  user.idm = "0114c4ff6a180701"
  user.webhook_url = "https://hooks.slack.com/services/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"

  session.add(user)
  session.commit()

if __name__ == "__main__":
  _main()
