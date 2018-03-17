import signal
import binascii
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

def _main():
  # for Ctrl-C
  signal.signal(signal.SIGINT, ctrlc_handler)

  target = 'usb:054c:02e1'
  reader = CardReader(target)
  while True:
    reader.ready()
    info = reader.get_info()
    if info is not None:
      print(info)

if __name__ == "__main__":
  _main()
