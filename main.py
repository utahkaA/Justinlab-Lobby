import signal
import binascii
import requests
import json

from db.session import Session
import nfc

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
  with Session() as sess:
    match_users = sess.query(User).filter(
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

  target = 'usb:054c:02e1'
  reader = CardReader(target)
  while True:
    reader.ready()
    info = reader.get_info()
    if info is not None:
      # notify(session, info)
      print(info)

if __name__ == "__main__":
  _main()
