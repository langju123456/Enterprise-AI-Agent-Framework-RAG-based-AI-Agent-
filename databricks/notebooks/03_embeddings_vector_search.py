# Databricks notebook: 03_embeddings_vector_search.py
# Replace fake embeddings with Bedrock embeddings + write to a table for Vector Search

import numpy as np
from pyspark.sql import functions as F, types as T

source_tbl = "silver.chunks"
target_tbl = "gold.chunks_with_vec"

def fake_embed(text):
    np.random.seed(abs(hash(text)) % (2**32))
    return [float(x) for x in np.random.rand(768)]

fake_embed_udf = F.udf(fake_embed, T.ArrayType(T.FloatType()))
chunks = spark.table(source_tbl)
with_vec = chunks.withColumn("embedding", fake_embed_udf(F.col("chunk_text")))
with_vec.write.mode("overwrite").saveAsTable(target_tbl)

print(f"Wrote embeddings to {target_tbl}. Now configure Databricks Vector Search to index this table.")
