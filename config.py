import os

# ==============================================================================
# Google BigQuery Configuration
# ==============================================================================
# Set the environment variable directly so the google-cloud SDK picks it up seamlessly
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\mdelcid\Desktop\jfc-ai-project.json"

BQ_PROJECT_ID = "jfc-ai-project"
BQ_DATASET_ID = "yelp"
BQ_TABLE_ID = "restaurant_review"

# ==============================================================================
# Smarty Address Verification SDK Configuration
# ==============================================================================
SMARTY_AUTH_ID = "your-smarty-auth-id"
SMARTY_AUTH_TOKEN = "your-smarty-auth-token"

# ==============================================================================
# Oracle Database Connection (python-oracledb Thin Mode)
# ==============================================================================
DB_USER = "your_oracle_user"
DB_PASSWORD = "your_oracle_password"
DB_DSN = "your-oracle-hostname:1521/your_service_name"