import os
import streamlit as st
from google.cloud import bigquery
import pandas as pd
import altair as alt

# --------------------------
# Set Google Application Credentials
# --------------------------
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\ASUS\OneDrive\Desktop\PythonProject\service-account.json"

# --------------------------
# Streamlit Page Config
# --------------------------
st.set_page_config(page_title="Supply Chain Dashboard", layout="wide")
st.title("📊 Supply Chain Data Integration System")

# --------------------------
# BigQuery Client
# --------------------------
client = bigquery.Client()

# --------------------------
# Query Data from BigQuery
# --------------------------
query = """
SELECT 
    d.year, 
    SUM(SAFE_CAST(REPLACE(REPLACE(f.Sales, "$", ""), ",", "") AS NUMERIC)) AS total_sales,
    SUM(SAFE_CAST(REPLACE(REPLACE(f.Profit, "$", ""), ",", "") AS NUMERIC)) AS total_profit
FROM `supplychainproject-488016.supply_chain_dataset.fact_orders` f
JOIN `supplychainproject-488016.supply_chain_dataset.dim_date` d
ON f.`Order Date` = d.date
GROUP BY d.year
ORDER BY d.year
"""

df = client.query(query).to_dataframe()

# --------------------------
# Ensure correct data types
# --------------------------
df['year'] = df['year'].astype(str)  # For Altair charts
df['total_sales'] = pd.to_numeric(df['total_sales'])
df['total_profit'] = pd.to_numeric(df['total_profit'])

# --------------------------
# Sidebar Filters
# --------------------------
st.sidebar.header("Filters")

if not df.empty:
    year_range = st.sidebar.slider(
        "Select Year Range",
        min_value=int(df['year'].min()),
        max_value=int(df['year'].max()),
        value=(int(df['year'].min()), int(df['year'].max()))
    )
    df = df[(df['year'].astype(int) >= year_range[0]) & (df['year'].astype(int) <= year_range[1])]
else:
    st.warning("No data found in BigQuery.")
    st.stop()

# --------------------------
# Show KPIs
# --------------------------
st.subheader("Overall Metrics")
col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${df['total_sales'].sum():,.2f}")
col2.metric("Total Profit", f"${df['total_profit'].sum():,.2f}")

# --------------------------
# Bar Chart: Sales Over Years
# --------------------------
st.subheader("Sales Over Years")
sales_chart = alt.Chart(df).mark_bar(color="#1f77b4").encode(
    x=alt.X('year:N', title='Year'),
    y=alt.Y('total_sales:Q', title='Sales ($)'),
    tooltip=[alt.Tooltip('year:N', title='Year'),
             alt.Tooltip('total_sales:Q', title='Sales', format="$,.2f")]
)
st.altair_chart(sales_chart, width='stretch')

# --------------------------
# Line Chart: Profit Over Years
# --------------------------
st.subheader("Profit Over Years")
profit_chart = alt.Chart(df).mark_line(point=True, color="#ff7f0e").encode(
    x=alt.X('year:N', title='Year'),
    y=alt.Y('total_profit:Q', title='Profit ($)'),
    tooltip=[alt.Tooltip('year:N', title='Year'),
             alt.Tooltip('total_profit:Q', title='Profit', format="$,.2f")]
)
st.altair_chart(profit_chart, width='stretch')

# --------------------------
# Combined Chart: Sales vs Profit
# --------------------------
st.subheader("Sales vs Profit (Combined)")
combined_chart = alt.Chart(df).transform_fold(
    ['total_sales', 'total_profit'],
    as_=['Metric', 'Value']
).mark_line(point=True).encode(
    x=alt.X('year:N', title='Year'),
    y=alt.Y('Value:Q', title='Amount ($)'),
    color=alt.Color('Metric:N', title='Metric'),
    tooltip=[alt.Tooltip('year:N', title='Year'),
             alt.Tooltip('Metric:N', title='Metric'),
             alt.Tooltip('Value:Q', title='Amount', format="$,.2f")]
)
st.altair_chart(combined_chart, width='stretch')

# --------------------------
# Data Table Preview
# --------------------------
st.subheader("Data Preview")
st.dataframe(df)