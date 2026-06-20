import random
from datetime import timedelta
import random
import pandas as pd
from pyspark.sql import SparkSession


spark = (
    SparkSession.builder
    .appName("GenerateTrainingData")
    .getOrCreate()
)

# Read Silver Data
silver_df = spark.read.parquet(
    "data_lake/silver/curated_sales"
)

base_df = silver_df.select(
    "category",
    "region",
    "revenue"
).toPandas()

# Generate 2 years of dates
dates = pd.date_range(
    start="2024-01-01",
    end="2025-12-31",
    freq="D"
)

training_data = []

regions = [
    "North",
    "South",
    "East",
    "West"
]

category_factor = {
    "Beverages": 1.30,
    "Dairy": 1.10,
    "Snacks": 0.90,
    "PersonalCare": 1.00
}

region_factor = {
    "South": 1.20,
    "East": 1.00,
    "North": 0.90,
    "West": 0.95
}

for _, row in base_df.iterrows():

    for current_date in dates:

        category = row["category"]

        region = random.choice(regions)

        revenue = row["revenue"]

        if current_date.month in [11, 12]:
            seasonal_factor = 1.20

        elif current_date.month in [6, 7]:
            seasonal_factor = 1.10

        else:
            seasonal_factor = 1.00

        random_factor = random.uniform(
            0.90,
            1.10
        )

        synthetic_revenue = round(
            revenue
            * category_factor[category]
            * region_factor[region]
            * seasonal_factor
            * random_factor,
            2
        )

        training_data.append(
            [
                current_date,
                category,
                region,
                synthetic_revenue
            ]
        )

training_df = pd.DataFrame(
    training_data,
    columns=[
        "event_date",
        "category",
        "region",
        "revenue"
    ]
)

training_df.to_parquet(
    "ml/training_sales.parquet",
    index=False
)

print(
    f"Training records generated: {len(training_df)}"
)