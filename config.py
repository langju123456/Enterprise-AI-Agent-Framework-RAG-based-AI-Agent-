"""
Configuration management for the Enterprise AI Agent Framework.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # AWS Configuration
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "us-east-1"
    aws_bedrock_model: str = "anthropic.claude-v2"
    
    # Databricks Configuration
    databricks_host: str = ""
    databricks_token: str = ""
    databricks_cluster_id: str = ""
    databricks_vector_search_endpoint: str = ""
    
    # MLflow Configuration
    mlflow_tracking_uri: str = "databricks"
    mlflow_experiment_name: str = "/Users/default/rag_experiment"
    
    # Delta Lake Configuration
    delta_table_raw: str = "raw_data"
    delta_table_silver: str = "silver_data"
    delta_table_gold: str = "gold_data"
    delta_database: str = "rag_database"
    
    # Application Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    streamlit_port: int = 8501
    
    # Embedding Model
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Vector Search Configuration
    vector_search_index: str = "rag_vector_index"
    vector_dimension: int = 384
    top_k_results: int = 5
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
