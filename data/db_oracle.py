import logging
from contextlib import closing

import oracledb

import config

logger = logging.getLogger(__name__)

oracledb.init_oracle_client(lib_dir=r"C:\Oracle\instantclient_21_23")

INSERT_CUSTOMER_YELP_SQL = """
    MERGE INTO K2.CUSTOMER_YELP target
    USING (
        SELECT :YELP_BID AS YELP_BID
        FROM dual
    ) source
    ON (target.YELP_BID = source.YELP_BID)
    WHEN NOT MATCHED THEN
        INSERT (
            YELP_BID,
            NAME,
            ADDRESS,
            CITY,
            STATE,
            ZIPCODE,
            COUNTRY,
            PHONENUMBER,
            SITEURL,
            VERIFIED_LATITUDE,
            VERIFIED_LONGITUDE,
            YELPLINK,
            DESCRIPTION
        )
        VALUES (
            source.YELP_BID,
            :NAME,
            :ADDRESS,
            :CITY,
            :STATE,
            :ZIPCODE,
            :COUNTRY,
            :PHONENUMBER,
            :SITEURL,
            :VERIFIED_LATITUDE,
            :VERIFIED_LONGITUDE,
            :YELPLINK,
            :DESCRIPTION
        )
"""


def insert_customer_yelp_records(records: list[dict]) -> int:
    """
    Inserts Yelp records into CUSTOMER_YELP in a single transaction.
    Returns the number of inserted rows.
    """
    if not records:
        logger.info("No CUSTOMER_YELP records to insert.")
        return 0

    logger.info("Opening Oracle connection...")
    try:
        with closing(
            oracledb.connect(
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                dsn=config.DB_DSN,
            )
        ) as connection:
            try:
                with connection.cursor() as cursor:
                    logger.info(
                        "Inserting %d records into K2.CUSTOMER_YELP...",
                        len(records),
                    )
                    cursor.executemany(INSERT_CUSTOMER_YELP_SQL, records)
                    inserted_count = cursor.rowcount

                connection.commit()
                logger.info("Oracle transaction committed successfully.")
                return inserted_count

            except Exception:
                connection.rollback()
                logger.exception("Insert failed. Oracle transaction rolled back.")
                raise

    except Exception:
        logger.exception("Oracle CUSTOMER_YELP import failed.")
        raise