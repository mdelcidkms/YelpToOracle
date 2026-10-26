import logging
from logging.handlers import RotatingFileHandler
import google.cloud.bigquery
import oracledb
import smartystreets_python_sdk
from data.bq_yelp import fetch_raw_yelp_records

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
print("Starting the Yelp to Oracle ETL process...")

def main():
    records = fetch_raw_yelp_records()

    print(f"Total records: {len(records)}")
    if records:
        print("First row:")
        print(records[0])  # full dict

        # optional: print just a few fields
        for i, row in enumerate(records[:5], start=1):
            print(f"{i}. {row.get('NAME')} | {row.get('CITY')}, {row.get('STATE')} | {row.get('YELP_BID')} | {row.get('VERIFIED_LATITUDE')} | {row.get('VERIFIED_LONGITUDE')}")

if __name__ == "__main__":
    main()