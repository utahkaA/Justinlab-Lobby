# !usr/bin/env python
# coding: utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
  'mysql+pymysql://root:mariadb@0.0.0.0:3306/justinlab?charset=utf8',
  echo=True)
Session = sessionmaker(bind=engine)
