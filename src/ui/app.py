import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import os

st.set_page_config(
    page_title="Sales Forecast Dashboard",
    layout="wide"
)

st.title("📈 Sales Forecast Dashboard")

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)
# -----------------------------
# Load Dropdown Values
# -----------------------------
categories = requests.get(
    f"{API_URL}/categories"
).json()

brands = requests.get(
    f"{API_URL}/brands"
).json()

regions = requests.get(
    f"{API_URL}/regions"
).json()

# -----------------------------
# Filters
# -----------------------------
selected_category = st.selectbox(
    "Category",
    ["All"] + categories
)

selected_brand = st.selectbox(
    "Brand",
    ["All"] + brands
)

selected_region = st.selectbox(
    "Region",
    ["All"] + regions
)

params = {}

if selected_category != "All":
    params["category"] = selected_category

if selected_brand != "All":
    params["brand"] = selected_brand

if selected_region != "All":
    params["region"] = selected_region

# -----------------------------
# Forecast Data
# -----------------------------
forecast = requests.get(
    f"{API_URL}/forecast",
    params=params
).json()

df = pd.DataFrame(forecast)

if df.empty:

    st.warning(
        "No forecast data available for the selected Category, Brand and Region combination."
    )

    st.stop()

# -----------------------------
# Summary Metrics
# -----------------------------
if not df.empty:

    top_category = (
        df.groupby("category")
        ["predicted_revenue"]
        .mean()
        .idxmax()
    )

    top_brand = (
        df.groupby("brand")["predicted_revenue"]
        .mean()
        .idxmax()
    )

    top_region = (
        df.groupby("region")
        ["predicted_revenue"]
        .mean()
        .idxmax()
    )

    avg_revenue = round(
        df["predicted_revenue"].mean(),
        2
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Top Category",
            top_category
        )

    with col2:
        st.metric(
            "Top Region",
            top_region
        )

    with col3:
        st.metric(
            "Average Revenue",
            f"${avg_revenue:,.2f}"
        )

# -----------------------------
# Forecast Table
# -----------------------------
st.subheader("Forecast Data")

st.dataframe(
    df,
    use_container_width=True
)

# -----------------------------
# Revenue Trend
# -----------------------------
if not df.empty:

    chart_df = (
        df.groupby("forecast_date")
        ["predicted_revenue"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        chart_df,
        x="forecast_date",
        y="predicted_revenue",
        title="Revenue Forecast Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -----------------------------
# Revenue by Category
# -----------------------------
if not df.empty:

    category_df = (
        df.groupby("category")
        ["predicted_revenue"]
        .mean()
        .reset_index()
    )

    st.subheader("Revenue by Category")

    st.bar_chart(
        category_df.set_index("category")
    )

# -----------------------------
# Revenue by Region
# -----------------------------
if not df.empty:

    region_df = (
        df.groupby("region")
        ["predicted_revenue"]
        .mean()
        .reset_index()
    )

    st.subheader("Revenue by Region")

    st.bar_chart(
        region_df.set_index("region")
    )

# -----------------------------
# Business Insights
# -----------------------------
st.subheader("Business Insights")

top_category = (
    df.groupby("category")["predicted_revenue"]
    .mean()
    .idxmax()
)

top_region = (
    df.groupby("region")["predicted_revenue"]
    .mean()
    .idxmax()
)

avg_revenue = round(
    df["predicted_revenue"].mean(),
    2
)

trend_df = (
    df.groupby("forecast_date")
    ["predicted_revenue"]
    .sum()
    .reset_index()
)

first_day = trend_df.iloc[0]["predicted_revenue"]
last_day = trend_df.iloc[-1]["predicted_revenue"]

change_pct = (
    (last_day - first_day)
    / first_day
) * 100

if change_pct > 5:
    trend_message = "Demand is expected to increase over the forecast period."

elif change_pct < -5:
    trend_message = "Demand is expected to decline over the forecast period."

else:
    trend_message = "Demand is expected to remain relatively stable over the forecast period."

st.success(
    f"""
    • Highest forecasted category: {top_category}

    • Highest forecasted brand: {top_brand}

    • Highest forecasted region: {top_region}

    • Average forecasted revenue: ${avg_revenue}

    • {trend_message}
    """
)

# -----------------------------
# AI Insights
# -----------------------------
st.subheader("AI Insights")

summary_text = f"""
Highest forecasted category: {top_category}

Highest forecasted region: {top_region}

Average forecasted revenue: {avg_revenue}

Trend: {trend_message}
"""

insights_response = requests.post(
    f"{API_URL}/insights",
    json={
        "summary_text": summary_text
    }
).json()

st.info(
    insights_response["insights"]
)