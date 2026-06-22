import streamlit as st
import pandas as pd
import plotly.express as px



product_df = pd.read_csv (r"C:\Users\DAHAMYA\PycharmProjects\PythonProject\retail_sales_pipeline\folder\State_01.csv")
region_df = pd.read_csv(r"C:\Users\DAHAMYA\PycharmProjects\PythonProject\retail_sales_pipeline\folder\State_01 (3).csv")
daily_df = pd.read_csv(r"C:\Users\DAHAMYA\PycharmProjects\PythonProject\retail_sales_pipeline\folder\State_01 (1).csv")

st.title("Retail Sales Lakehouse Dashboard")
st.subheader("Revenue by Product")

st.dataframe(product_df)

st.subheader("Key Metrics")

st.metric("Total Rows", len(product_df))
st.metric("Columns", len(product_df.columns))

st.write(product_df.columns)

st.subheader("Revenue by Product")

if "TotalRevenue" in product_df.columns:
    fig = px.bar(product_df, x="Product", y="TotalRevenue", color="Product")
    st.plotly_chart(fig)
else:
    st.error("TotalRevenue column not found in dataset")

##Region Analysis

st.write(region_df.columns)
st.subheader("Revenue by Region")

region_summary = region_df.groupby("Region")["TotalRevenue"].sum().reset_index()

fig = px.bar(region_summary, x="Region", y="TotalRevenue", color="Region")
st.plotly_chart(fig)

##Daily Trend

daily_df["Date"] = pd.to_datetime(daily_df["Date"])

daily_summary = daily_df.groupby("Date")["DailyRevenue"].sum().reset_index()

st.subheader("Daily Revenue Trend")

fig = px.line(daily_summary, x="Date", y="DailyRevenue")
st.plotly_chart(fig)

st.sidebar.title("Filters")

product_list = product_df["Product"].unique()
selected_product = st.sidebar.selectbox("Select Product", product_list)

filtered_df = product_df[product_df["Product"] == selected_product]

st.subheader("Filtered Product Data")
st.dataframe(filtered_df)