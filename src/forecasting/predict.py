import pandas as pd
import joblib

# Load training data
df = pd.read_parquet(
    "ml/training_sales.parquet"
)

# Get categories and regions
categories = df["category"].unique()
regions = df["region"].unique()

# Get last date
last_date = df["event_date"].max()

# Generate next 30 days
future_dates = pd.date_range(
    start=last_date + pd.Timedelta(days=1),
    periods=30,
    freq="D"
)

# Load model and feature columns
model = joblib.load(
    "ml/artifacts/revenue_forecast.pkl"
)

model_columns = joblib.load(
    "ml/artifacts/model_columns.pkl"
)

prediction_rows = []

for forecast_date in future_dates:

    for category in categories:

        for region in regions:

            feature_row = {
                "month": forecast_date.month,
                "day_of_week": forecast_date.dayofweek
            }

            # Initialize all model columns to 0
            for column in model_columns:
                if column not in feature_row:
                    feature_row[column] = 0

            # Set category dummy column
            category_column = f"category_{category}"

            if category_column in feature_row:
                feature_row[category_column] = 1

            # Set region dummy column
            region_column = f"region_{region}"

            if region_column in feature_row:
                feature_row[region_column] = 1

            # Create dataframe in exact training order
            X = pd.DataFrame([feature_row])

            X = X[model_columns]

            predicted_revenue = model.predict(X)[0]

            prediction_rows.append(
                {
                    "forecast_date": forecast_date,
                    "category": category,
                    "region": region,
                    "predicted_revenue": round(
                        predicted_revenue,
                        2
                    )
                }
            )

forecast_df = pd.DataFrame(
    prediction_rows
)

forecast_df.to_parquet(
    "ml/predictions/forecast.parquet",
    index=False
)

print(forecast_df.head())

print(
    f"\nForecast records generated: {len(forecast_df)}"
)