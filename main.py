import signal
import binascii
import requests
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import nfc
from models.users import User

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

def notify(session, info):
  idm = info["idm"]
  match_users = session.query(User).filter(
    User.idm == idm
  ).all()
  target_user = match_users[0]
  requests.post(target_user.webhook_url, data=json.dumps({
    "text": "[Test] Touch and Go",
    "username": "Justinlab",
    "icon_emoji": ":gopher",
    "link_names": 1,
  }))

def _main():
  # for Ctrl-C
  signal.signal(signal.SIGINT, ctrlc_handler)

  # for Database
  db_url = "mysql+pymysql://root:mariadb@0.0.0.0:3306/justinlab?charset=utf8"
  engine = create_engine(db_url)
  session = scoped_session(
    sessionmaker(
      autocommit = False,
      autoflush = False,
      bind = engine
    )
  )

  target = 'usb:054c:02e1'
  reader = CardReader(target)
  while True:
    reader.ready()
    info = reader.get_info()
    if info is not None:
      notify(session, info)

if __name__ == "__main__":
  _main()
