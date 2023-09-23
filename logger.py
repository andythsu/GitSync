import logging
import os
def set_logging():
  logging.basicConfig(level=logging.DEBUG if os.environ.get("debug", "false") == "true" else logging.INFO,
                      format="%(levelname)s: %(message)s")
