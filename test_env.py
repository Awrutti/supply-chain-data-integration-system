import os
from dotenv import load_dotenv

load_dotenv()

print("Project ID:", os.getenv("GCP_PROJECT_ID"))