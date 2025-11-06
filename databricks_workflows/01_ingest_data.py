# Databricks notebook source
# MAGIC %md
# MAGIC # Data Ingestion - Raw Layer
# MAGIC 
# MAGIC This notebook ingests raw data into the Delta Lake Raw table.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, lit
from datetime import datetime
import uuid

# Get parameters from job
dbutils.widgets.text("database", "rag_database")
dbutils.widgets.text("table", "raw_data")

database = dbutils.widgets.get("database")
table_name = dbutils.widgets.get("table")
full_table_name = f"{database}.{table_name}"

print(f"Target table: {full_table_name}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create Database and Table

# COMMAND ----------

# Create database if not exists
spark.sql(f"CREATE DATABASE IF NOT EXISTS {database}")

# Create raw Delta table
spark.sql(f"""
CREATE TABLE IF NOT EXISTS {full_table_name} (
    id STRING,
    content STRING,
    metadata STRING,
    source STRING,
    ingestion_timestamp TIMESTAMP
) USING DELTA
PARTITIONED BY (source)
""")

print(f"Table {full_table_name} ready")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Ingest Sample Data

# COMMAND ----------

# Sample data for demonstration
sample_data = [
    {
        "id": str(uuid.uuid4()),
        "content": "Enterprise AI Agent Framework is a scalable RAG-based system.",
        "metadata": '{"type": "documentation", "category": "architecture"}',
        "source": "documentation"
    },
    {
        "id": str(uuid.uuid4()),
        "content": "The framework integrates LangChain, AWS Bedrock, and Databricks.",
        "metadata": '{"type": "documentation", "category": "integration"}',
        "source": "documentation"
    },
    {
        "id": str(uuid.uuid4()),
        "content": "Delta Lake provides ACID transactions for data reliability.",
        "metadata": '{"type": "documentation", "category": "data"}',
        "source": "documentation"
    }
]

# Create DataFrame
df = spark.createDataFrame(sample_data)
df = df.withColumn("ingestion_timestamp", current_timestamp())

# Write to Delta table
df.write.format("delta").mode("append").saveAsTable(full_table_name)

print(f"Ingested {df.count()} records")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Verify Ingestion

# COMMAND ----------

# Display ingested data
display(spark.table(full_table_name))

# COMMAND ----------

# Show table stats
spark.sql(f"DESCRIBE DETAIL {full_table_name}").show()
