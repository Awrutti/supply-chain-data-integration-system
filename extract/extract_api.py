import requests
import pandas as pd

def extract_api():
    url = "https://fakestoreapi.com/products"
    response = requests.get(url)
    df = pd.DataFrame(response.json())
    print("API Extracted")
    return df

if __name__ == "__main__":
    extract_api()