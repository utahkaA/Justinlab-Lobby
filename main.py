# !/usr/bin/env python
# coding: utf-8
import signal
import time
from datetime import datetime, timedelta
import requests
import json

import sqlalchemy as sa

from utils import get_logger, ctrlc_handler
from app.io import CardReader
from db.session import Session
from db.models import User, Card, Log

def classify(info):
  idm = info["idm"]
  with Session() as sess:
    try:
      match_card = sess.query(Card).filter(
        Card.idm == idm
      ).first()
      print(">>> student id: {0}".format(match_card.stuid))
      res = match_card.stuid
    except sa.exc.OperationalError as err:
      print(err)
      res = None
    except Exception as err:
      print(err.args)
      res = None
  return res

def notify(stuid, status):
  with Session() as sess:
    match_user = sess.query(User).filter(
      User.stuid == stuid
    ).first()

    if status == "login":
      msg = "[Login] {0} が研究室に入室しました。".format(match_user.name)
    else:
      msg = "[Logout] {0} が研究室から退室しました。".format(match_user.name)

    r = requests.post(match_user.webhook, data=json.dumps({
      "text": msg,
      "username": "Justinlab",
      "link_names": 1,
    }))
    return True

def insert_log(stuid, timestamp):
  with Session() as sess:
    # get a last log record
    last_log = sess.query(Log).filter(
      Log.stuid == stuid
    ).order_by(
      sa.desc(Log.timestamp)
    ).first()

    # set status (login or logout)
    if last_log is not None:
      now_dt = datetime.fromtimestamp(timestamp)
      last_dt = datetime.fromtimestamp(last_log.timestamp)
      diff = now_dt.date() - last_dt.date()
      if (diff.days >= 1) and (last_log.status == "login"):
        # force logout feature
        last_datetime = datetime.fromtimestamp(last_log.timestamp)
        logout_date = last_datetime.date() + timedelta(days=1)
        timestamp = time.mktime(logout_date.timetuple())
        # insert force logout log
        sess.add(Log(
          stuid=stuid,
          timestamp=timestamp,
          status="logout",
          is_touched=False,
        ))
        status = "login"
      else:
        status = "login" if last_log.status == "logout" else "logout"

    log = Log(
      stuid=stuid,
      timestamp=timestamp,
      status=status,
      is_touched=True,
    )
    sess.add(log)
    sess.commit()
  return status

def _main():
  # for Ctrl-C
  signal.signal(signal.SIGINT, ctrlc_handler)

  # get logger
  logger = get_logger(__name__)
  logger.info("start Justinlab")

  target = 'usb:054c:02e1'
  reader = CardReader(target)
  logger.info("card reader start")
  while True:
    reader.ready()
    logger.info("waiting for being touched by a card...")

    info, timestamp = reader.get_info()
    logger.info(info)
    if info is not None:
      stuid = classify(info)
      logger.info(stuid)
      if stuid is None:
        continue

      status = insert_log(stuid, timestamp)
      if notify(stuid, status):
        logger.info("succeeded posting message to Slack")
      else:
        logger.info("failed posting message to Slack")

if __name__ == "__main__":
  _main()
