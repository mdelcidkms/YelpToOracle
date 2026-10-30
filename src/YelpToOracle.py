import logging
from logging.handlers import RotatingFileHandler
import google.cloud.bigquery
import oracledb
import smartystreets_python_sdk
from data.bq_yelp import fetch_raw_yelp_records
from data.db_oracle import insert_customer_yelp_records

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

logger = logging.getLogger(__name__)


print("All dependencies imported successfully!!")
print("Starting the Yelp to Oracle ETL process...")

def main():
    logger.info("Starting Yelp -> Oracle import flow.")

    records = fetch_raw_yelp_records()
    total_extracted = len(records)
    logger.info("BigQuery extraction completed. Rows fetched: %d", total_extracted)
    print(f"BigQuery rows fetched: {total_extracted}")

    if total_extracted == 0:
        logger.warning("No rows extracted from BigQuery. Import skipped.")
        print("No rows returned from BigQuery. Nothing to insert.")
        return

    try:
        inserted_count = insert_customer_yelp_records(records)
        logger.info(
            "CUSTOMER_YELP insert completed successfully. Rows inserted: %d",
            inserted_count,
        )
        print(f"SUCCESS: Inserted {inserted_count} row(s) into CUSTOMER_YELP.")
    except Exception as err:
        logger.error("CUSTOMER_YELP import failed: %s", err, exc_info=True)
        print("ERROR: Oracle import failed. Check logs for details.")

if __name__ == "__main__":
    main()