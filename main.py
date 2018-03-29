# !/usr/bin/env python
# coding: utf-8
import signal
import binascii
import requests
import json

import nfc

from db.session import Session
from db.models import User, Card

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
      return self.info
    else:
      return None

def notify(info):
  idm = info["idm"]
  with Session() as sess:
    match_card = sess.query(Card).filter(
      Card.idm == idm
    ).first()

    print(">>> student id: {0}".format(match_card.stuid))

    match_user = sess.query(User).filter(
      User.stuid == match_card.stuid
    ).first()

    msg = "[Login] {0} が研究室に入室しました。".format(match_user.name)
    requests.post(match_user.webhook, data=json.dumps({
      "text": msg,
      "username": "Justinlab",
      "link_names": 1,
    }))

def _main():
  # for Ctrl-C
  signal.signal(signal.SIGINT, ctrlc_handler)

  target = 'usb:054c:02e1'
  reader = CardReader(target)
  while True:
    reader.ready()
    info = reader.get_info()
    if info is not None:
      notify(info)
      # print(info)

if __name__ == "__main__":
  _main()
