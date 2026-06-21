from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    StringType,
    DoubleType
)

sales_schema = StructType([
    StructField("transaction_id", IntegerType(), False),
    StructField("date", StringType(), True),
    StructField("sku", StringType(), True),
    StructField("store_id", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("price", DoubleType(), True)
])

products_schema = StructType([
    StructField("sku", StringType(), False),
    StructField("category", StringType(), True),
    StructField("brand", StringType(), True),
    StructField("package_size", StringType(), True),
    StructField("list_price", DoubleType(), True),
    StructField("launch_date", StringType(), True)
])

stores_schema = StructType([
    StructField("store_id", StringType(), False),
    StructField("store_name", StringType(), True),
    StructField("region", StringType(), True),
    StructField("demographic_segment", StringType(), True)
])