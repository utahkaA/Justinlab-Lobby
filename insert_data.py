# !/usr/bin/env python
# coding: utf-8
import signal
import time
import sys

import nfc

from db.session import Session
from db.models import User, Card
from main import ctrlc_handler, CardReader

def insert_record(stuid, name, webhook, info):
  with Session() as sess:
    user = User(
      stuid=stuid,
      name=name,
      webhook=webhook,
      created_at=time.time(),
      updated_at=time.time(),
    )
    card = Card(
      stuid=stuid,
      idm=info["idm"],
      pmm=info["pmm"],
      sys=info["sys"],
      created_at=time.time(),
      updated_at=time.time(),
    )
    sess.add(user)
    sess.add(card)
    sess.commit()

def _main():
  # for Ctrl-C
  signal.signal(signal.SIGINT, ctrlc_handler)

  stuid = sys.argv[1]
  name = sys.argv[2]
  webhook = sys.argv[3]
  print(">>> plz, touch {0} {1}'s card".format(stuid, name))
  print(">>> webhook url: {0}".format(webhook))

  target = 'usb:054c:02e1'
  reader = CardReader(target)
  reader.ready()
  info, _ = reader.get_info()
  if info is not None:
    insert_record(stuid, name, webhook, info)

if __name__ == "__main__":
  _main()
