
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Retail Sales Analysis Dashboard",
    layout="wide"
)

st.title("Retail Sales Analysis Dashboard")
st.write("Explore retail sales performance interactively.")

@st.cache_data
def load_data():
    return pd.read_csv("retail_sales_dataset.csv")

df = load_data()

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

total_sales = df["Total Amount"].sum()
total_orders = df["Transaction ID"].nunique()
quantity_sold = df["Quantity"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"{total_sales:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Quantity Sold", f"{quantity_sold:,}")

st.subheader("Filter Sales")

gender = st.multiselect(
    "Select Gender",
    sorted(df["Gender"].dropna().unique()),
    default=sorted(df["Gender"].dropna().unique())
)

categories = st.multiselect(
    "Select Product Category",
    sorted(df["Product Category"].dropna().unique()),
    default=sorted(df["Product Category"].dropna().unique())
)

filtered = df[
    df["Gender"].isin(gender)
    & df["Product Category"].isin(categories)
].copy()

st.subheader("Sales by Product Category")
category_sales = filtered.groupby(
    "Product Category"
)["Total Amount"].sum().sort_values(ascending=False)
st.bar_chart(category_sales)

st.subheader("Monthly Sales Trend")
monthly = (
    filtered.dropna(subset=["Date"])
    .set_index("Date")["Total Amount"]
    .resample("MS").sum()
)
st.line_chart(monthly)

st.subheader("Sales by Gender")
gender_sales = filtered.groupby("Gender")["Total Amount"].sum()
st.bar_chart(gender_sales)

st.subheader("Filtered Transaction Data")
st.dataframe(filtered, use_container_width=True)
