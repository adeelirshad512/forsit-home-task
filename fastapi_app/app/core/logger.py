import os
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("app_logger")
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logger.setLevel(getattr(logging, log_level, logging.INFO))

log_format = "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
formatter = logging.Formatter(log_format)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, 'app.log')

file_handler = RotatingFileHandler(log_path, maxBytes=5_000_000, backupCount=3)
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)
