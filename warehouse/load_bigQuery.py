from google.cloud import bigquery
from google.oauth2 import service_account

PROJECT_ID = "supplychainproject-488016"
DATASET_ID = "supply_chain_dataset"

def load_table(df, table_name):

    credentials = service_account.Credentials.from_service_account_file(
        "service-account.json"
    )

    client = bigquery.Client(
        credentials=credentials,
        project=PROJECT_ID,
    )

    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

    job = client.load_table_from_dataframe(df, table_id)
    job.result()

    print(f"{table_name} loaded to BigQuery")