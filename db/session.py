# !usr/bin/env python
# coding: utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
  'mysql+pymysql://root:mariadb@0.0.0.0:3306/justinlab?charset=utf8',
  echo=True)
Sess = sessionmaker(bind=engine, autocommit=False)

class Session(object):
  def __init__(self):
    self.session = Sess()

  def __enter__(self):
    return self.session

  def __exit__(self, *exception):
    if exception[0] is not None:
      self.session.rollback()
    self.session.close()
