from fastapi import FastAPI
import pandas as pd
from src.llm.generate_insights import generate_insights
from pydantic import BaseModel

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
    brand: str = None,
    region: str = None
):

    df = pd.read_parquet(
        "ml/predictions/forecast.parquet"
    )

    if category:
        df = df[
            df["category"] == category
        ]

    if brand:
        df = df[
            df["brand"] == brand
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

        "top_brand": (
            df.groupby("brand")["predicted_revenue"]
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

@app.get("/brands")
def get_brands():

    df = pd.read_parquet(
        "ml/predictions/forecast.parquet"
    )

    return sorted(
        df["brand"].unique().tolist()
    )

    
@app.get("/regions")
def get_regions():

    df = pd.read_parquet(
        "ml/predictions/forecast.parquet"
    )

    return sorted(
        df["region"].unique().tolist()
    )

class InsightRequest(BaseModel):
    summary_text: str


@app.post("/insights")
def get_insights(request: InsightRequest):

    insights = generate_insights(
        request.summary_text
    )

    return {
        "insights": insights
    }