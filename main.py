from extract.extract_csv import extract_csv
from extract.extract_api import extract_api
from staging.mysql_stage import stage_to_mysql
from transform.transform_star_schema import build_star_schema
from warehouse.load_bigQuery import load_table
from warehouse.marts import create_marts

def run_pipeline():

    csv_df = extract_csv()
    api_df = extract_api()

    stage_to_mysql(csv_df, "superstore_stage")
    stage_to_mysql(api_df, "api_products_stage")

    fact, cust, prod, date = build_star_schema(csv_df)

    load_table(fact, "fact_orders")
    load_table(cust, "dim_customer")
    load_table(prod, "dim_product")
    load_table(date, "dim_date")

    create_marts()

if __name__ == "__main__":
    run_pipeline()