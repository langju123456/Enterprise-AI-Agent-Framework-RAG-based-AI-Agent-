# Databricks notebook: 01_ingest_cleaning.py
from pyspark.sql import functions as F

s3_path = "s3://your-bucket/docs/"
bronze_tbl = "bronze.raw_docs"

df = spark.read.format("binaryFile").load(s3_path)
df = df.select("path", "modificationTime", "length")
df = df.withColumn("text", F.lit("placeholder text parsed from document"))

df.write.mode("overwrite").saveAsTable(bronze_tbl)
print(f"Ingested to {bronze_tbl}")
