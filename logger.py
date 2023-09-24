import logging
import os
from logging import debug as logging_debug, info as logging_info

def set_logging():
  is_debug_on = os.environ.get("debug_mode", "false") == "true"
  print("is_debug_on", is_debug_on)
  logging.basicConfig(level=logging.DEBUG if is_debug_on else logging.INFO,
                      format="%(levelname)s: %(message)s" if is_debug_on else "%(message)s")
def debug(msg, data):
  logging_debug(f"{msg}: {data}")

def info(msg: str, *args):
  if args:
    logging_info(f"{msg}: {' '.join(args)}")
  else:
    logging_info(f"{msg}")
