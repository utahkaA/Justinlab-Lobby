# !/usr/bin/env python
# coding: utf-8
import signal
import time
import binascii
import requests
import json

import sqlalchemy as sa
import nfc

from db.session import Session
from db.models import User, Card, Log

def ctrlc_handler(signal, frame):
  print("\nKeyboardInterrupt")
  exit()

class CardReader():
  def __init__(self, target):
    self.target = target
    self.info = dict()

  def on_connect(self, tag):
    """
    Card touch handler funcion
    """
    self.info = {
      "idm": binascii.hexlify(tag.idm),
      "pmm": binascii.hexlify(tag.pmm),
      "sys": tag.sys
    }
    return True

  def ready(self):
    with nfc.ContactlessFrontend(self.target) as clf:
      clf.connect(rdwr={'on-connect': self.on_connect})

  def get_info(self):
    if self.info.viewkeys() >= {"idm", "pmm", "sys"}:
      return self.info, time.time()
    else:
      return None

def classify(info):
  idm = info["idm"]
  with Session() as sess:
    match_card = sess.query(Card).filter(
      Card.idm == idm
    ).first()
    print(">>> student id: {0}".format(match_card.stuid))
  return match_card.stuid

def notify(stuid):
  with Session() as sess:
    match_user = sess.query(User).filter(
      User.stuid == stuid
    ).first()

    msg = "[Login] {0} が研究室に入室しました。".format(match_user.name)
    requests.post(match_user.webhook, data=json.dumps({
      "text": msg,
      "username": "Justinlab",
      "link_names": 1,
    }))

def insert_log(stuid, timestamp):
  with Session() as sess:
    # get a last log record
    last_log = sess.query(Log).filter(
      Log.stuid == stuid
    ).order_by(
      sa.desc(Log.timestamp)
    ).first()

    # set status (login or logout)
    is_touched = True
    status = "login"
    if last_log is not None:
      # 1日以上のブランクを許さない処理
      # このとき is_touched = False
      is_touched = True
      status = "login" if last_log.status == "logout" else "logout"

    log = Log(
      stuid=stuid,
      timestamp=timestamp,
      status=status,
      is_touched=is_touched,
    )
    sess.add(log)
    sess.commit()

def _main():
  # for Ctrl-C
  signal.signal(signal.SIGINT, ctrlc_handler)

  target = 'usb:054c:02e1'
  reader = CardReader(target)
  while True:
    reader.ready()
    info, timestamp = reader.get_info()
    if info is not None:
      stuid = classify(info)
      notify(stuid)
      insert_log(stuid, timestamp)

if __name__ == "__main__":
  _main()
