# Databricks notebook source
# MAGIC %md
# MAGIC # Generate Embeddings
# MAGIC 
# MAGIC This notebook generates embeddings for documents using Sentence-BERT.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import pandas_udf, col
from pyspark.sql.types import ArrayType, FloatType
import pandas as pd
from sentence_transformers import SentenceTransformer

# Get parameters
dbutils.widgets.text("model", "sentence-transformers/all-MiniLM-L6-v2")
dbutils.widgets.text("table", "silver_data")

model_name = dbutils.widgets.get("model")
table_name = dbutils.widgets.get("table")
full_table = f"rag_database.{table_name}"

print(f"Model: {model_name}")
print(f"Table: {full_table}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Load Embedding Model

# COMMAND ----------

# Broadcast the model to all workers
model = SentenceTransformer(model_name)

@pandas_udf(ArrayType(FloatType()))
def generate_embeddings(content_series: pd.Series) -> pd.Series:
    """Generate embeddings for a batch of documents."""
    model = SentenceTransformer(model_name)
    texts = content_series.tolist()
    embeddings = model.encode(texts, convert_to_numpy=True)
    return pd.Series([embedding.tolist() for embedding in embeddings])

print("Embedding function ready")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Generate and Update Embeddings

# COMMAND ----------

# Read silver table
silver_df = spark.table(full_table)

# Filter records without embeddings
records_to_process = silver_df.filter(col("embeddings").isNull())

if records_to_process.count() > 0:
    # Generate embeddings
    embedded_df = records_to_process.withColumn(
        "embeddings", 
        generate_embeddings(col("content"))
    )
    
    # Update table using merge
    embedded_df.createOrReplaceTempView("embedded_updates")
    
    spark.sql(f"""
    MERGE INTO {full_table} AS target
    USING embedded_updates AS source
    ON target.id = source.id
    WHEN MATCHED THEN UPDATE SET target.embeddings = source.embeddings
    """)
    
    print(f"Generated embeddings for {records_to_process.count()} records")
else:
    print("All records already have embeddings")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Verify Embeddings

# COMMAND ----------

# Check embedding statistics
result = spark.sql(f"""
SELECT 
    COUNT(*) as total_records,
    SUM(CASE WHEN embeddings IS NOT NULL THEN 1 ELSE 0 END) as records_with_embeddings,
    AVG(size(embeddings)) as avg_embedding_dimension
FROM {full_table}
""")

display(result)

# COMMAND ----------

# Display sample
display(spark.table(full_table).select("id", "content", "embeddings").limit(5))
