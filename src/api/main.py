from fastapi import FastAPI
import pandas as pd
from src.llm.generate_insights import generate_insights


app = FastAPI(
    title="Sales Forecast API",
    version="1.0.0"
)


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.get("/forecast")
def get_forecast(
    category: str = None,
    region: str = None
):

    df = pd.read_parquet(
        "ml/predictions/forecast.parquet"
    )

    if category:
        df = df[
            df["category"] == category
        ]

    if region:
        df = df[
            df["region"] == region
        ]

    return df.to_dict(
        orient="records"
    )


@app.get("/summary")
def get_summary():

    df = pd.read_parquet(
        "ml/predictions/forecast.parquet"
    )

    return {
        "top_category": (
            df.groupby("category")["predicted_revenue"]
            .mean()
            .idxmax()
        ),

        "top_region": (
            df.groupby("region")["predicted_revenue"]
            .mean()
            .idxmax()
        ),

        "average_forecast_revenue": round(
            df["predicted_revenue"].mean(),
            2
        ),

        "max_forecast_revenue": round(
            df["predicted_revenue"].max(),
            2
        ),

        "min_forecast_revenue": round(
            df["predicted_revenue"].min(),
            2
        ),

        "forecast_days": 30
    }

@app.get("/categories")
def get_categories():

    df = pd.read_parquet(
        "ml/predictions/forecast.parquet"
    )

    return sorted(
        df["category"].unique().tolist()
    )


@app.get("/regions")
def get_regions():

    df = pd.read_parquet(
        "ml/predictions/forecast.parquet"
    )

    return sorted(
        df["region"].unique().tolist()
    )

@app.get("/insights")
def get_insights():

    summary_text = """
    Top Category: Beverages
    Top Region: South
    Average Revenue: 1237.71
    Revenue Trend: Increasing
    """

    insights = generate_insights(summary_text)

    return {
        "insights": insights
    }