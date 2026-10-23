import logging
from logging.handlers import RotatingFileHandler
import google.cloud.bigquery
import oracledb
import smartystreets_python_sdk

# Create handlers
console_handler = logging.StreamHandler()
file_handler = RotatingFileHandler(
    "yelp_to_oracle.log",   # log file name
    maxBytes=5 * 1024 * 1024,  # 5 MB per file
    backupCount=5,             # keep 5 old files
    encoding="utf-8"
)

# Shared format
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Root logger setup
logging.basicConfig(
    level=logging.INFO,
    handlers=[console_handler, file_handler]
)

print("All dependencies imported successfully!!")