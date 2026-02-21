 #Step 1: Tell Python where your Google service account JSON is
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\ASUS\Desktop\service-account.json"

# Step 2: Now import BigQuery client
from google.cloud import bigquery

# Step 3: Connect to BigQuery
client = bigquery.Client()

# Step 4: Test query
query = "SELECT CURRENT_DATE()"
df = client.query(query).to_dataframe()
print(df)