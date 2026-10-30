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
    "yelp_to_oracle.log",      # log file name
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
    logger.info("Starting Yelp -> Oracle import.")

    try:
        records = fetch_raw_yelp_records()
        total_records = len(records)

        logger.info("Source records returned: %d", total_records)

        if not records:
            logger.warning(
                "No source records returned; Oracle import skipped. "
                "Check extraction logs for any source errors."
            )
            return

        inserted_count = insert_customer_yelp_records(records)
        skipped_count = total_records - inserted_count

        logger.info(
            "SUCCESS: CUSTOMER_YELP import committed. "
            "Received: %d | Inserted: %d | Skipped (existing YELP_BID): %d",
            total_records,
            inserted_count,
            skipped_count,
        )

    except Exception:
        logger.exception("FAILED: Yelp -> Oracle import did not complete.")
        raise


if __name__ == "__main__":
    main()