# Databricks notebook source
# MAGIC %md
# MAGIC # Data Processing - Silver Layer
# MAGIC 
# MAGIC This notebook processes data from Raw to Silver layer with cleaning and validation.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, trim, col, lit
from pyspark.sql.types import FloatType

# Get parameters
dbutils.widgets.text("database", "rag_database")
dbutils.widgets.text("silver_table", "silver_data")

database = dbutils.widgets.get("database")
raw_table = f"{database}.raw_data"
silver_table = f"{database}.{dbutils.widgets.get('silver_table')}"

print(f"Source table: {raw_table}")
print(f"Target table: {silver_table}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create Silver Table

# COMMAND ----------

spark.sql(f"""
CREATE TABLE IF NOT EXISTS {silver_table} (
    id STRING,
    content STRING,
    embeddings ARRAY<FLOAT>,
    metadata STRING,
    source STRING,
    processing_timestamp TIMESTAMP,
    quality_score FLOAT
) USING DELTA
PARTITIONED BY (source)
""")

print(f"Table {silver_table} ready")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Process and Clean Data

# COMMAND ----------

# Read from raw table
raw_df = spark.table(raw_table)

# Data cleaning and transformation
silver_df = raw_df.select(
    col("id"),
    trim(col("content")).alias("content"),
    col("metadata"),
    col("source")
).withColumn("processing_timestamp", current_timestamp()) \
 .withColumn("quality_score", lit(1.0).cast(FloatType())) \
 .withColumn("embeddings", lit(None).cast("array<float>"))

# Filter out already processed records
existing_ids = spark.table(silver_table).select("id")
new_records = silver_df.join(existing_ids, "id", "left_anti")

# Write to silver table
if new_records.count() > 0:
    new_records.write.format("delta").mode("append").saveAsTable(silver_table)
    print(f"Processed {new_records.count()} new records")
else:
    print("No new records to process")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Verify Processing

# COMMAND ----------

# Display silver data
display(spark.table(silver_table))

# COMMAND ----------

# Show statistics
spark.sql(f"SELECT source, COUNT(*) as count FROM {silver_table} GROUP BY source").show()
