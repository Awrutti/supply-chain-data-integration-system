import pandas as pd

def extract_csv():
    df = pd.read_csv("data/superstore.csv", encoding="latin1")
    print("CSV Extracted")
    return df
if __name__ == "__main__":
    extract_csv()