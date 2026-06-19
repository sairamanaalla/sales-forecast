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
    StructField("region", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("price", DoubleType(), True)
])

products_schema = StructType([
    StructField("sku", StringType(), False),
    StructField("category", StringType(), True),
    StructField("brand", StringType(), True)
])

stores_schema = StructType([
    StructField("store_id", IntegerType(), False),
    StructField("region", StringType(), True)
])