from google.cloud import bigquery
import os
from dotenv import load_dotenv

load_dotenv()

project_id = os.getenv("GCP_PROJECT_ID")
client = bigquery.Client(project=project_id)

print("Connected to project:", client.project)
