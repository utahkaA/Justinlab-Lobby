# !/usr/bin/env python
# coding: utf-8
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR, DATETIME
from db.session import Session

Base = declarative_base()

class User(Base):
  __tablename__ = "users"

  id = Column('id', BIGINT(unsigned=True), primary_key=True)
  stuid = Column('stuid', VARCHAR(7), nullable=False)
  name = Column('name', VARCHAR(50), nullable=False)
  webhook = Column('webhook', VARCHAR(2100), nullable=False)
  created_at = Column('created_at', DATETIME, nullable=False)
  updated_at = Column('updated_at', DATETIME, nullable=False)

  @classmethod
  def find(cls, id):
    session = Session()
    record = session.query(User).filter(User.id == id).first()
    session.close()
    return record
