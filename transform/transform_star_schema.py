import pandas as pd

def build_star_schema(df):

    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])
    df["Lead_Time"] = (df["Ship Date"] - df["Order Date"]).dt.days

    # DIM DATE
    dim_date = pd.DataFrame({
        "date": df["Order Date"].unique()
    })
    dim_date["year"] = pd.to_datetime(dim_date["date"]).dt.year
    dim_date["month"] = pd.to_datetime(dim_date["date"]).dt.month

    # DIM CUSTOMER
    dim_customer = df[[
        "Customer ID",
        "Customer Name",
        "Segment",
        "Region",
        "Country"
    ]].drop_duplicates()

    # DIM PRODUCT
    dim_product = df[[
        "Product ID",
        "Product Name",
        "Category",
        "Sub-Category"
    ]].drop_duplicates()

    


    # FACT TABLE
    fact_orders = df[[
        "Product ID",
        "Customer ID",
        "Order Date",
        "Sales",
        "Quantity",
        "Profit",
        "Discount",
        "Shipping Cost",
        "Lead_Time"
    ]]
    # Clean numeric columns


    print("Star Schema Built")

    return fact_orders, dim_customer, dim_product, dim_date
