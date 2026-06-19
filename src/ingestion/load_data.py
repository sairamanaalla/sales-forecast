from pyspark.sql import SparkSession

from pyspark.sql.functions import current_timestamp,lit

from schemas import (
    sales_schema,
    products_schema,
    stores_schema
)

from validation import validate_columns


spark = (
    SparkSession.builder
    .appName("Ingestion")
    .getOrCreate()
)

# Reading Raw files from data/raw

sales_df = (
    spark.read
    .schema(sales_schema)
    .option("header", "true")
    .csv("data/raw/sales.csv")
)

products_df = (
    spark.read
    .schema(products_schema)
    .option("header", "true")
    .csv("data/raw/products.csv")
)

stores_df = (
    spark.read
    .schema(stores_schema)
    .option("header", "true")
    .csv("data/raw/stores.csv")
)

# Schema Validation

validate_columns(
    sales_df,
    [
        "transaction_id",
        "date",
        "sku",
        "region",
        "quantity",
        "price"
    ]
)

# Lineage Metadata

sales_df = (
    sales_df
    .withColumn("source_file", lit("sales.csv"))
    .withColumn(
        "ingestion_timestamp",
        current_timestamp()
    )
)

products_df = (
    products_df
    .withColumn("source_file", lit("products.csv"))
    .withColumn(
        "ingestion_timestamp",
        current_timestamp()
    )
)

stores_df = (
    stores_df
    .withColumn("source_file", lit("stores.csv"))
    .withColumn(
        "ingestion_timestamp",
        current_timestamp()
    )
)

# Bronze Layer

sales_df.write.mode("overwrite").parquet(
    "data_lake/bronze/sales"
)

products_df.write.mode("overwrite").parquet(
    "data_lake/bronze/products"
)

stores_df.write.mode("overwrite").parquet(
    "data_lake/bronze/stores"
)

print("Bronze layer created successfully")