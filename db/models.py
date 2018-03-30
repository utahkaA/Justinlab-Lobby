# !/usr/bin/env python
# coding: utf-8
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from session import Session

Base = declarative_base()

class User(Base):
  """
  definition of the 'users' table
  """
  __tablename__ = "users"

  stuid = sa.Column('stuid', sa.String(7), primary_key=True, nullable=False)
  name = sa.Column('name', sa.String(50), nullable=False)
  webhook = sa.Column('webhook', sa.String(2100), nullable=False)
  created_at = sa.Column('created_at', sa.String(13), nullable=False)
  updated_at = sa.Column('updated_at', sa.String(13), nullable=False)

  cards = relationship("Card", back_populates="users")
  logs = relationship("Log", back_populates="users")

  @classmethod
  def find(cls, id):
    with Session() as sess:
      record = sess.query(User).filter(User.id == id).first()
    return record

class Card(Base):
  """
  definition of the 'cards' table
  """
  __tablename__ = 'cards'

  id = sa.Column("id", sa.Integer, primary_key=True)
  stuid = sa.Column("stuid", sa.String(7), sa.ForeignKey("users.stuid"),
                    unique=True, nullable=False)
  idm = sa.Column("idm", sa.String(64), nullable=False)
  pmm = sa.Column("pmm", sa.String(64), nullable=False)
  sys = sa.Column("sys", sa.String(64), nullable=False)
  created_at = sa.Column('created_at', sa.Integer, nullable=False)
  updated_at = sa.Column('updated_at', sa.Integer, nullable=False)

  users = relationship("User", back_populates="cards")

class Log(Base):
  """
  definition of the 'logs' table
  """
  __tablename__ = 'logs'
  id = sa.Column("id", sa.Integer, primary_key=True)
  stuid = sa.Column("stuid", sa.String(7), sa.ForeignKey("users.stuid"),
                    unique=True, nullable=False)
  timestamp = sa.Column("timestamp", sa.Integer, nullable=False)
  status = sa.Column("status", sa.String(6), nullable=False)
  is_touched = sa.Column("is_touched", sa.Boolean, nullable=False)

  users = relationship("User", back_populates="logs")
