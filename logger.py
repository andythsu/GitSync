import logging
import os
from logging import debug as logging_debug, info as logging_info
def set_logging():
  logging.basicConfig(level=logging.DEBUG if os.environ.get("debug", "false") == "true" else logging.INFO,
                      format="%(levelname)s: %(message)s")
def debug(msg, data):
  logging_debug(f"{msg}: {data}")

def info(msg):
  logging_info(msg)
