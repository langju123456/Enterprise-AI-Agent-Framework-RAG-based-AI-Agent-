# Databricks notebook: 02_chunking_delta.py
from pyspark.sql import functions as F
bronze_tbl = "bronze.raw_docs"
silver_tbl = "silver.chunks"

raw = spark.table(bronze_tbl)
chunks = raw.select(
    F.col("path").alias("doc_path"),
    F.col("text").alias("chunk_text"),
    F.lit(0).alias("chunk_id")
)
chunks.write.mode("overwrite").saveAsTable(silver_tbl)
print(f"Chunked to {silver_tbl}")
