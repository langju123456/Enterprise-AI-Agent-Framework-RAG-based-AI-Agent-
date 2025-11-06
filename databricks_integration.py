"""
Databricks Lakehouse integration with Delta Tables and MLflow.
"""
from typing import List, Dict, Any, Optional
import mlflow
from datetime import datetime
from config import settings


class DeltaTableManager:
    """Manager for Delta Lake tables (Raw, Silver, Gold)."""
    
    def __init__(self):
        """Initialize Delta table manager."""
        self.database = settings.delta_database
        self.raw_table = f"{self.database}.{settings.delta_table_raw}"
        self.silver_table = f"{self.database}.{settings.delta_table_silver}"
        self.gold_table = f"{self.database}.{settings.delta_table_gold}"
    
    def create_raw_table(self, spark_session) -> str:
        """
        Create raw data Delta table.
        
        Args:
            spark_session: Active Spark session
            
        Returns:
            Table creation status
        """
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS {self.raw_table} (
            id STRING,
            content TEXT,
            metadata STRING,
            source STRING,
            ingestion_timestamp TIMESTAMP,
            CONSTRAINT raw_pk PRIMARY KEY (id)
        ) USING DELTA
        PARTITIONED BY (source)
        """
        
        # This would execute in actual Databricks environment
        # spark_session.sql(create_sql)
        return f"Raw table {self.raw_table} created"
    
    def create_silver_table(self, spark_session) -> str:
        """
        Create silver (cleaned/processed) data Delta table.
        
        Args:
            spark_session: Active Spark session
            
        Returns:
            Table creation status
        """
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS {self.silver_table} (
            id STRING,
            content TEXT,
            embeddings ARRAY<FLOAT>,
            metadata STRING,
            source STRING,
            processing_timestamp TIMESTAMP,
            quality_score FLOAT,
            CONSTRAINT silver_pk PRIMARY KEY (id)
        ) USING DELTA
        PARTITIONED BY (source)
        """
        
        # This would execute in actual Databricks environment
        # spark_session.sql(create_sql)
        return f"Silver table {self.silver_table} created"
    
    def create_gold_table(self, spark_session) -> str:
        """
        Create gold (analytics-ready) data Delta table.
        
        Args:
            spark_session: Active Spark session
            
        Returns:
            Table creation status
        """
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS {self.gold_table} (
            id STRING,
            aggregated_content TEXT,
            topic STRING,
            category STRING,
            embedding_vector ARRAY<FLOAT>,
            metadata STRING,
            creation_timestamp TIMESTAMP,
            usage_count INT,
            CONSTRAINT gold_pk PRIMARY KEY (id)
        ) USING DELTA
        PARTITIONED BY (topic)
        """
        
        # This would execute in actual Databricks environment
        # spark_session.sql(create_sql)
        return f"Gold table {self.gold_table} created"
    
    def insert_raw_data(self, data: List[Dict[str, Any]], spark_session) -> int:
        """
        Insert data into raw Delta table.
        
        Args:
            data: List of records to insert
            spark_session: Active Spark session
            
        Returns:
            Number of records inserted
        """
        # In production, convert to DataFrame and write to Delta
        # df = spark_session.createDataFrame(data)
        # df.write.format("delta").mode("append").saveAsTable(self.raw_table)
        return len(data)
    
    def promote_to_silver(self, spark_session) -> str:
        """
        Promote and transform data from Raw to Silver.
        
        Args:
            spark_session: Active Spark session
            
        Returns:
            Promotion status
        """
        transform_sql = f"""
        INSERT INTO {self.silver_table}
        SELECT 
            id,
            TRIM(content) as content,
            NULL as embeddings,  -- Will be populated by embedding pipeline
            metadata,
            source,
            CURRENT_TIMESTAMP() as processing_timestamp,
            1.0 as quality_score
        FROM {self.raw_table}
        WHERE id NOT IN (SELECT id FROM {self.silver_table})
        """
        
        # This would execute in actual Databricks environment
        # spark_session.sql(transform_sql)
        return f"Data promoted from {self.raw_table} to {self.silver_table}"
    
    def promote_to_gold(self, spark_session) -> str:
        """
        Aggregate and promote data from Silver to Gold.
        
        Args:
            spark_session: Active Spark session
            
        Returns:
            Promotion status
        """
        transform_sql = f"""
        INSERT INTO {self.gold_table}
        SELECT 
            id,
            content as aggregated_content,
            'general' as topic,
            source as category,
            embeddings as embedding_vector,
            metadata,
            CURRENT_TIMESTAMP() as creation_timestamp,
            0 as usage_count
        FROM {self.silver_table}
        WHERE id NOT IN (SELECT id FROM {self.gold_table})
        """
        
        # This would execute in actual Databricks environment
        # spark_session.sql(transform_sql)
        return f"Data promoted from {self.silver_table} to {self.gold_table}"


class MLflowPipelineManager:
    """MLflow integration for pipeline tracking and scheduling."""
    
    def __init__(self):
        """Initialize MLflow manager."""
        mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
        mlflow.set_experiment(settings.mlflow_experiment_name)
    
    def start_pipeline_run(self, pipeline_name: str, parameters: Dict[str, Any]) -> str:
        """
        Start a new MLflow run for pipeline execution.
        
        Args:
            pipeline_name: Name of the pipeline
            parameters: Pipeline parameters
            
        Returns:
            Run ID
        """
        run = mlflow.start_run(run_name=pipeline_name)
        mlflow.log_params(parameters)
        mlflow.set_tag("pipeline_name", pipeline_name)
        mlflow.set_tag("start_time", datetime.now().isoformat())
        return run.info.run_id
    
    def log_pipeline_metrics(self, metrics: Dict[str, float]) -> None:
        """
        Log pipeline metrics to MLflow.
        
        Args:
            metrics: Dictionary of metric names and values
        """
        mlflow.log_metrics(metrics)
    
    def log_pipeline_artifacts(self, artifact_path: str, artifact_name: str) -> None:
        """
        Log pipeline artifacts to MLflow.
        
        Args:
            artifact_path: Path to the artifact file
            artifact_name: Name for the artifact
        """
        mlflow.log_artifact(artifact_path, artifact_name)
    
    def end_pipeline_run(self, status: str = "FINISHED") -> None:
        """
        End the current MLflow run.
        
        Args:
            status: Run status (FINISHED, FAILED, KILLED)
        """
        mlflow.set_tag("end_time", datetime.now().isoformat())
        mlflow.set_tag("status", status)
        mlflow.end_run()
    
    def get_run_info(self, run_id: str) -> Dict[str, Any]:
        """
        Get information about a specific run.
        
        Args:
            run_id: MLflow run ID
            
        Returns:
            Run information dictionary
        """
        run = mlflow.get_run(run_id)
        return {
            "run_id": run.info.run_id,
            "experiment_id": run.info.experiment_id,
            "status": run.info.status,
            "start_time": run.info.start_time,
            "end_time": run.info.end_time,
            "metrics": run.data.metrics,
            "params": run.data.params,
            "tags": run.data.tags
        }


class DatabricksJobScheduler:
    """Databricks Jobs scheduling for automated pipeline execution."""
    
    def __init__(self):
        """Initialize Databricks job scheduler."""
        self.host = settings.databricks_host
        self.token = settings.databricks_token
    
    def create_rag_pipeline_job(self) -> Dict[str, Any]:
        """
        Create a scheduled job for RAG pipeline execution.
        
        Returns:
            Job configuration
        """
        job_config = {
            "name": "RAG_Pipeline_Scheduled_Job",
            "tasks": [
                {
                    "task_key": "ingest_raw_data",
                    "description": "Ingest raw data into Delta table",
                    "notebook_task": {
                        "notebook_path": "/Workflows/ingest_data",
                        "base_parameters": {
                            "database": settings.delta_database,
                            "table": settings.delta_table_raw
                        }
                    }
                },
                {
                    "task_key": "process_to_silver",
                    "description": "Process and clean data to Silver table",
                    "depends_on": [{"task_key": "ingest_raw_data"}],
                    "notebook_task": {
                        "notebook_path": "/Workflows/process_silver",
                        "base_parameters": {
                            "database": settings.delta_database,
                            "silver_table": settings.delta_table_silver
                        }
                    }
                },
                {
                    "task_key": "generate_embeddings",
                    "description": "Generate embeddings for documents",
                    "depends_on": [{"task_key": "process_to_silver"}],
                    "notebook_task": {
                        "notebook_path": "/Workflows/generate_embeddings",
                        "base_parameters": {
                            "model": settings.embedding_model,
                            "table": settings.delta_table_silver
                        }
                    }
                },
                {
                    "task_key": "promote_to_gold",
                    "description": "Aggregate and promote to Gold table",
                    "depends_on": [{"task_key": "generate_embeddings"}],
                    "notebook_task": {
                        "notebook_path": "/Workflows/promote_gold",
                        "base_parameters": {
                            "database": settings.delta_database,
                            "gold_table": settings.delta_table_gold
                        }
                    }
                }
            ],
            "schedule": {
                "quartz_cron_expression": "0 0 2 * * ?",  # Daily at 2 AM
                "timezone_id": "UTC"
            },
            "max_concurrent_runs": 1
        }
        
        # In production, use Databricks SDK to create the job
        # from databricks.sdk import WorkspaceClient
        # w = WorkspaceClient()
        # job = w.jobs.create(**job_config)
        
        return job_config
    
    def trigger_job_run(self, job_id: str) -> str:
        """
        Manually trigger a job run.
        
        Args:
            job_id: Databricks job ID
            
        Returns:
            Run ID
        """
        # In production, trigger via Databricks SDK
        # from databricks.sdk import WorkspaceClient
        # w = WorkspaceClient()
        # run = w.jobs.run_now(job_id=job_id)
        # return run.run_id
        
        return f"job_run_{job_id}_{datetime.now().timestamp()}"
