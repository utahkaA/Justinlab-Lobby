#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
  main(debug='False',
       url='mysql+pymysql://root:mariadb@0.0.0.0:3306/justinlab?charset=utf8',
       repository='.')
