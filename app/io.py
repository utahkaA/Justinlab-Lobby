import binascii
import nfc

class CardReader():
  def __init__(self, target):
    self.target = target
    self.info = dict()
    self.tag_type = None

  def on_connect(self, tag):
    """
    Card touch handler funcion
    """
    try:
      self.tag_type = type(tag)
      self.info = {
        "idm": binascii.hexlify(tag.idm),
        "pmm": binascii.hexlify(tag.pmm),
        "sys": tag.sys
      }
    except AttributeError as err:
      return False
    return True

  def ready(self):
    with nfc.ContactlessFrontend(self.target) as clf:
      clf.connect(rdwr={'on-connect': self.on_connect})

  def get_info(self):
    if self.info.viewkeys() >= {"idm", "pmm", "sys"}:
      return self.info
    else:
      return None
