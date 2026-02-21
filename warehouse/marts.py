from google.cloud import bigquery
from google.oauth2 import service_account

PROJECT_ID = "supplychainproject-488016"
DATASET_ID = "supply_chain_dataset"

def create_marts():

    credentials = service_account.Credentials.from_service_account_file(
        "service-account.json"
    )

    client = bigquery.Client(
        credentials=credentials,
        project=PROJECT_ID,
    )

    query = f"""
CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.sales_summary` AS
SELECT
    d.year,
    SUM(
        CAST(
            REPLACE(REPLACE(f.sales, '$', ''), ',', '')
        AS FLOAT64)
    ) AS total_sales,
    SUM(
        CAST(
            REPLACE(REPLACE(f.profit, '$', ''), ',', '')
        AS FLOAT64)
    ) AS total_profit
FROM `{PROJECT_ID}.{DATASET_ID}.fact_orders` f
JOIN `{PROJECT_ID}.{DATASET_ID}.dim_date` d
    ON DATE(f.`Order Date`) = DATE(d.date)
GROUP BY d.year
"""

    client.query(query).result()

    print("Data Mart Created: sales_summary")