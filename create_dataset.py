from google.cloud import bigquery
import os
from dotenv import load_dotenv

load_dotenv()

project_id = os.getenv("GCP_PROJECT_ID")

client = bigquery.Client(project=project_id)

dataset_id = f"{project_id}.supply_chain_dataset"

dataset = bigquery.Dataset(dataset_id)
dataset.location = "US"

dataset = client.create_dataset(dataset, exists_ok=True)

print(f"Dataset created successfully: {dataset_id}")