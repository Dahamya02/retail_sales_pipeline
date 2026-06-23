# Databricks notebook source
# MAGIC %sql
# MAGIC SHOW CATALOGS;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW CATALOGS;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW SCHEMAS IN retail_sales;

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG retail_sales;
# MAGIC USE SCHEMA lakehouse;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW VOLUMES IN retail_sales.lakehouse;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW VOLUMES;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW SCHEMAS;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW VOLUMES IN retail_sales.lakehouse;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT current_catalog(), current_schema();

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS bronze_sales;

# COMMAND ----------

df = spark.read.csv(
    "/Volumes/retail_sales/lakehouse/retail_sales_volume/retail_sales_data.csv",
    header=True
)


# COMMAND ----------

display(df)

# COMMAND ----------

df.printSchema()

# COMMAND ----------

df.count()

# COMMAND ----------

df.count()

# COMMAND ----------


from pyspark.sql.functions import col, sum, when

df.select([
    sum(when(col(c).isNull(), 1).otherwise(0)).alias(c)
    for c in df.columns
]).show()

# COMMAND ----------

df_clean = df.dropna()

# COMMAND ----------

df_clean = df.fillna({
    "Quantity": 0,
    "Price": 0,
    "Product": "Unknown"
})

# COMMAND ----------

df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("retail_sales.lakehouse.bronze_sales")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM retail_sales.lakehouse.bronze_sales
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN retail_sales.lakehouse;

# COMMAND ----------

bronze_df = spark.table("retail_sales.lakehouse.bronze_sales")

bronze_df.printSchema()

# COMMAND ----------

display(bronze_df.limit(5))

# COMMAND ----------

silver_df = bronze_df.dropDuplicates()

# COMMAND ----------

silver_df = silver_df.fillna({
    "Product": "Unknown",
    "Quantity": 0,
    "Price": 0
})

# COMMAND ----------

from pyspark.sql.functions import col

silver_df = silver_df.withColumn(
    "Revenue",
    col("Quantity") * col("Price")
)

# COMMAND ----------

bronze_df = spark.table("retail_sales.lakehouse.bronze_sales")

print(bronze_df.columns)

# COMMAND ----------

from pyspark.sql.functions import col, to_date

bronze_df = spark.table(
    "retail_sales.lakehouse.bronze_sales"
)

# COMMAND ----------

silver_df = bronze_df.dropDuplicates()

# COMMAND ----------

silver_df = silver_df.fillna({
    "Product": "Unknown",
    "City": "Unknown",
    "Region": "Unknown",
    "Price": 0,
    "Quantity": 0
})

# COMMAND ----------

silver_df = silver_df.withColumn(
    "Date",
    to_date(col("Date"))
)

# COMMAND ----------

silver_df = silver_df.withColumn(
    "Revenue",
    col("Price") * col("Quantity")
)

# COMMAND ----------

silver_df.printSchema()

# COMMAND ----------

bronze_df.printSchema()

# COMMAND ----------

from pyspark.sql.functions import col, to_date

bronze_df = spark.table(
    "retail_sales.lakehouse.bronze_sales"
)

# COMMAND ----------

silver_df = bronze_df.dropDuplicates()

# COMMAND ----------

silver_df = silver_df.fillna({
    "Product": "Unknown",
    "City": "Unknown",
    "Region": "Unknown",
    "Price": "0",
    "Quantity": "0"
})

# COMMAND ----------

from pyspark.sql.types import DoubleType, IntegerType

silver_df = silver_df.withColumn(
    "Price",
    col("Price").cast(DoubleType())
)

silver_df = silver_df.withColumn(
    "Quantity",
    col("Quantity").cast(IntegerType())
)

# COMMAND ----------

silver_df = silver_df.withColumn(
    "Date",
    to_date(col("Date"))
)

# COMMAND ----------

silver_df.printSchema()

# COMMAND ----------

display(silver_df)

# COMMAND ----------

from pyspark.sql.functions import col

# COMMAND ----------

from pyspark.sql.functions import col

bronze_df = spark.table("retail_sales.lakehouse.bronze_sales")

bronze_df.select("Price", "Quantity").show(20, False)

# COMMAND ----------

from pyspark.sql.functions import col
from pyspark.sql.types import DoubleType

silver_df = silver_df.withColumn(
    "Price",
    col("Price").cast(DoubleType())
)

silver_df = silver_df.withColumn(
    "Quantity",
    col("Quantity").cast(DoubleType())
)

# COMMAND ----------

silver_df = silver_df.fillna({
    "Price": 0.0,
    "Quantity": 0.0,
    "Product": "Unknown",
    "City": "Unknown",
    "Region": "Unknown"
})

# COMMAND ----------

silver_df = silver_df.withColumn(
    "Revenue",
    col("Price") * col("Quantity")
)

# COMMAND ----------

display(
    silver_df.select(
        "Product",
        "Price",
        "Quantity",
        "Revenue"
    )
)

# COMMAND ----------

silver_df.printSchema()

# COMMAND ----------

silver_df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("retail_sales.lakehouse.silver_sales")

# COMMAND ----------

from pyspark.sql.functions import sum

silver_df = spark.table("retail_sales.lakehouse.silver_sales")

gold_product = silver_df.groupBy("Product") \
    .agg(
        sum("Revenue").alias("TotalRevenue")
    )

display(gold_product)

# COMMAND ----------

gold_product.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("retail_sales.lakehouse.gold_product_revenue")

# COMMAND ----------

gold_region = silver_df.groupBy("Region") \
    .agg(
        sum("Revenue").alias("TotalRevenue")
    )

display(gold_region)

# COMMAND ----------

gold_region.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("retail_sales.lakehouse.gold_region_revenue")

# COMMAND ----------

gold_daily = silver_df.groupBy("Date") \
    .agg(
        sum("Revenue").alias("DailyRevenue")
    )

display(gold_daily)

# COMMAND ----------

gold_daily.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("retail_sales.lakehouse.gold_daily_revenue")

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN retail_sales.lakehouse;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM retail_sales.lakehouse.gold_product_revenue
# MAGIC ORDER BY TotalRevenue DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM retail_sales.lakehouse.gold_region_revenue
# MAGIC ORDER BY TotalRevenue DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM retail_sales.lakehouse.gold_daily_revenue
# MAGIC ORDER BY Date;

# COMMAND ----------

from pyspark.sql.functions import sum

silver_df = spark.table("retail_sales.lakehouse.silver_sales")

gold_product = silver_df.groupBy("Product") \
    .agg(sum("Revenue").alias("TotalRevenue"))

display(gold_product)

# COMMAND ----------

gold_product.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("retail_sales.lakehouse.gold_product_revenue")

# COMMAND ----------

gold_region = silver_df.groupBy("Region") \
    .agg(sum("Revenue").alias("TotalRevenue"))

display(gold_region)

# COMMAND ----------

gold_region.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("retail_sales.lakehouse.gold_region_revenue")

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN retail_sales.lakehouse;

# COMMAND ----------

from pyspark.sql.functions import sum

gold_product_quantity = silver_df.groupBy("Product") \
    .agg(sum("Quantity").alias("TotalUnitsSold"))

display(gold_product_quantity)

# COMMAND ----------

gold_product_quantity.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable("retail_sales.lakehouse.gold_product_quantity")

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN retail_sales.lakehouse;

# COMMAND ----------

gold_product = spark.table(
    "retail_sales.lakehouse.gold_product_revenue"
)

display(gold_product)

# COMMAND ----------

gold_product = spark.table(
    "retail_sales.lakehouse.gold_daily_revenue"
)

display(gold_product)