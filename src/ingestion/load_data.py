from pyspark.sql import SparkSession

from pyspark.sql.functions import *

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

print("Starting Bronze Layer Creation")

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
        "store_id",
        "quantity",
        "price"
    ]
)

validate_columns(
    products_df,
    [
        "sku",
        "category",
        "brand",
        "package_size",
        "list_price",
        "launch_date"
    ]
)

validate_columns(
    stores_df,
    [
        "store_id",
        "store_name",
        "region",
        "demographic_segment"
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

#-----------------------------------------
# SIlver Layer Creation 
#-----------------------------------------

print("Starting Silver Layer Creation")

bronze_sales_df = spark.read.parquet(
    "data_lake/bronze/sales"
)

bronze_products_df = spark.read.parquet(
    "data_lake/bronze/products"
)

bronze_stores_df = spark.read.parquet(
    "data_lake/bronze/stores"
)

bronze_sales_df = bronze_sales_df.withColumn(
    "event_date",
    expr("try_to_timestamp(date, 'yyyy-MM-dd')").cast("date")
)

# Data Quality Checks and Rejections

invalid_condition = (
    col("transaction_id").isNull()
    | col("sku").isNull()
    | col("store_id").isNull()
    | col("event_date").isNull()
    | col("quantity").isNull()
    | col("price").isNull()
    | (col("quantity") <= 0)
    | (col("price") <= 0)
)

rejected_sales_df = bronze_sales_df.filter(
    invalid_condition
)

valid_sales_df = bronze_sales_df.filter(
    ~invalid_condition
)

valid_sales_df = valid_sales_df.dropDuplicates(
    ["transaction_id"]
)

valid_sales_df = valid_sales_df.withColumn(
    "revenue",
    col("quantity") * col("price")
)

curated_sales_df = (
    valid_sales_df
    .join(
        bronze_products_df.select(
            "sku",
            "category",
            "brand",
            "package_size",
            "list_price",
            "launch_date"
        ),
        on="sku",
        how="left"
    )
    .join(
        bronze_stores_df.select(
            "store_id",
            "store_name",
            "region",
            "demographic_segment"
        ),
        on="store_id",
        how="left"
    )
)

rejected_reference_df = curated_sales_df.filter(
    col("category").isNull()
    | col("store_name").isNull()
)

curated_sales_df = curated_sales_df.filter(
    col("category").isNotNull()
    & col("store_name").isNotNull()
)

# Write Silver Layer

curated_sales_df.write.mode("overwrite").parquet("data_lake/silver/curated_sales")

rejected_sales_df.write.mode("overwrite").parquet("data_lake/silver/rejected_sales")

print(f"Curated Records: {curated_sales_df.count()}")

print(f"Rejected Records: {rejected_sales_df.count()}")

print("Silver layer created successfully")