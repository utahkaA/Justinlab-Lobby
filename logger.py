import os
import datetime
from logging import getLogger, Formatter, FileHandler, StreamHandler, DEBUG

today = datetime.date.today()
today = today.strftime("%Y%m%d")

path_to_log = "{0}/log/{1}.log".format(os.path.dirname(__file__), today)
fmt = "%(asctime)s %(name)s %(lineno)d [%(levelname)s][%(funcName)s] %(message)s"
log_fmt = Formatter(fmt)

def get_logger(module_name):
  logger = getLogger(module_name)
  handler = StreamHandler()
  handler.setLevel("INFO")
  handler.setFormatter(log_fmt)
  logger.addHandler(handler)

  handler = FileHandler(path_to_log, 'a')
  handler.setLevel(DEBUG)
  handler.setFormatter(log_fmt)
  logger.setLevel(DEBUG)
  logger.addHandler(handler)

  return logger
