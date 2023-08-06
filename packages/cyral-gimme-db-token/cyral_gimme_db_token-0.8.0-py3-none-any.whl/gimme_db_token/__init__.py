import logging
import sys

logger = logging.getLogger("gimme_db_token")
logger.setLevel(logging.INFO)
log_format = "%(asctime)s - - %(funcName)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(log_format)
handler = logging.StreamHandler(sys.stderr)
logger.addHandler(handler)
