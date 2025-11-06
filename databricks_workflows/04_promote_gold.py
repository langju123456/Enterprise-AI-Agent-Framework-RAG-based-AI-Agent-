# Databricks notebook source
# MAGIC %md
# MAGIC # Promote to Gold Layer
# MAGIC 
# MAGIC This notebook aggregates and promotes data from Silver to Gold layer.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, col, lit

# Get parameters
dbutils.widgets.text("database", "rag_database")
dbutils.widgets.text("gold_table", "gold_data")

database = dbutils.widgets.get("database")
silver_table = f"{database}.silver_data"
gold_table = f"{database}.{dbutils.widgets.get('gold_table')}"

print(f"Source table: {silver_table}")
print(f"Target table: {gold_table}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create Gold Table

# COMMAND ----------

spark.sql(f"""
CREATE TABLE IF NOT EXISTS {gold_table} (
    id STRING,
    aggregated_content STRING,
    topic STRING,
    category STRING,
    embedding_vector ARRAY<FLOAT>,
    metadata STRING,
    creation_timestamp TIMESTAMP,
    usage_count INT
) USING DELTA
PARTITIONED BY (topic)
""")

print(f"Table {gold_table} ready")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Aggregate and Promote Data

# COMMAND ----------

# Read from silver table
silver_df = spark.table(silver_table)

# Filter records with embeddings
ready_records = silver_df.filter(col("embeddings").isNotNull())

# Transform to gold schema
gold_df = ready_records.select(
    col("id"),
    col("content").alias("aggregated_content"),
    lit("general").alias("topic"),
    col("source").alias("category"),
    col("embeddings").alias("embedding_vector"),
    col("metadata")
).withColumn("creation_timestamp", current_timestamp()) \
 .withColumn("usage_count", lit(0))

# Filter out already promoted records
existing_ids = spark.table(gold_table).select("id")
new_records = gold_df.join(existing_ids, "id", "left_anti")

# Write to gold table
if new_records.count() > 0:
    new_records.write.format("delta").mode("append").saveAsTable(gold_table)
    print(f"Promoted {new_records.count()} records to gold layer")
else:
    print("No new records to promote")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Verify Gold Layer

# COMMAND ----------

# Display gold data
display(spark.table(gold_table))

# COMMAND ----------

# Show statistics by topic and category
spark.sql(f"""
SELECT 
    topic,
    category,
    COUNT(*) as record_count,
    AVG(size(embedding_vector)) as avg_embedding_dim
FROM {gold_table}
GROUP BY topic, category
""").show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Pipeline Summary

# COMMAND ----------

# Generate pipeline summary
summary = spark.sql(f"""
SELECT 
    'Raw' as layer,
    COUNT(*) as record_count
FROM {database}.raw_data
UNION ALL
SELECT 
    'Silver' as layer,
    COUNT(*) as record_count
FROM {database}.silver_data
UNION ALL
SELECT 
    'Gold' as layer,
    COUNT(*) as record_count
FROM {database}.gold_data
""")

display(summary)
