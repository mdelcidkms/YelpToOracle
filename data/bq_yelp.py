import logging
from google.cloud import bigquery
from google.cloud.exceptions import GoogleCloudError
import config
from contextlib import closing

logger = logging.getLogger(__name__)


def fetch_raw_yelp_records():
    """
    Extracts raw restaurant and customer rows directly from the source BigQuery table.

    Returns:
        list of dict: A lightweight collection of records, where each record is a
                      standard Python dictionary mapping Column -> Value.
    """
    table_path = f"`{config.BQ_PROJECT_ID}.{config.BQ_DATASET_ID}.{config.BQ_TABLE_ID}`"

    # Explicit column selection to prevent footprint bloat
    query = f"""
        SELECT business_id as YELP_BID, name as NAME, ARRAY_TO_STRING([
            NULLIF(JSON_VALUE(location.address, '$[0]'), ''),
            NULLIF(JSON_VALUE(location.address, '$[1]'), '')
            ], ', ') AS ADDRESS, location.city as CITY, location.state as STATE, location.postal_code as ZIPCODE, location.country as COUNTRY,
            phone as PHONENUMBER, business_url as SITEURL, location.coordinate.latitude as VERIFIED_LATITUDE, location.coordinate.longitude as VERIFIED_LONGITUDE,
            yelp_url as YELPLINK, attributes.AboutThisBizBio as DESCRIPTION
        FROM {table_path} 
        WHERE location.state = 'CA'
    """

    logger.info("Initializing BigQuery Client context...")

    try:
        # Context manager guarantees session teardown
        with closing(bigquery.Client(project=config.BQ_PROJECT_ID)) as bq_client:
            logger.info("Executing BigQuery extraction query.")
            query_job = bq_client.query(query)
            results = query_job.result()

            # Convert internal BQ Row objects to native dicts immediately.
            # This decouples downstream layers from Google-specific datatypes.
            records = [dict(row) for row in results]

            logger.info(f"Successfully extracted {len(records)} records from BigQuery.")
            return records

    except GoogleCloudError as gcp_err:
        logger.error(f"Google Cloud SDK error encountered: {gcp_err}", exc_info=True)
        return []
    except Exception as err:
        logger.error(
            f"Unexpected system crash during BigQuery extract: {err}", exc_info=True
        )
        return []
