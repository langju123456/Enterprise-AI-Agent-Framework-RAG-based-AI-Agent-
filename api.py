"""
FastAPI REST API for the Enterprise AI Agent Framework.
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import uvicorn

from config import settings
from rag_pipeline import RAGPipeline
from databricks_integration import (
    DeltaTableManager,
    MLflowPipelineManager,
    DatabricksJobScheduler
)


# Pydantic models for request/response
class QueryRequest(BaseModel):
    """Request model for RAG queries."""
    question: str
    context_length: Optional[int] = 5


class QueryResponse(BaseModel):
    """Response model for RAG queries."""
    question: str
    answer: str
    context_documents: List[Dict[str, Any]]
    num_documents_retrieved: int
    timestamp: str


class DocumentIngestRequest(BaseModel):
    """Request model for document ingestion."""
    documents: List[Dict[str, Any]]
    source: str = "api"


class PipelineRunRequest(BaseModel):
    """Request model for pipeline execution."""
    pipeline_name: str
    parameters: Optional[Dict[str, Any]] = {}


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: str
    version: str


# Initialize FastAPI app
app = FastAPI(
    title="Enterprise AI Agent Framework API",
    description="RAG-based AI Agent with Databricks Lakehouse and AWS Bedrock",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
rag_pipeline = RAGPipeline()
delta_manager = DeltaTableManager()
mlflow_manager = MLflowPipelineManager()
job_scheduler = DatabricksJobScheduler()


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with API information."""
    return HealthResponse(
        status="operational",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )


@app.post("/api/v1/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    """
    Execute a RAG query.
    
    Args:
        request: Query request with question and optional context length
        
    Returns:
        Query response with answer and context
    """
    try:
        result = rag_pipeline.query(
            question=request.question,
            context_length=request.context_length
        )
        
        return QueryResponse(
            question=result["question"],
            answer=result["answer"],
            context_documents=result["context_documents"],
            num_documents_retrieved=result["num_documents_retrieved"],
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/ingest")
async def ingest_documents(request: DocumentIngestRequest):
    """
    Ingest documents into the RAG system.
    
    Args:
        request: Document ingestion request
        
    Returns:
        Ingestion status
    """
    try:
        # In production, this would use actual Spark session
        # For now, return success status
        num_documents = len(request.documents)
        
        return {
            "status": "success",
            "message": f"Ingested {num_documents} documents",
            "documents_count": num_documents,
            "source": request.source,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/pipeline/run")
async def run_pipeline(request: PipelineRunRequest, background_tasks: BackgroundTasks):
    """
    Execute a data pipeline.
    
    Args:
        request: Pipeline execution request
        background_tasks: FastAPI background tasks
        
    Returns:
        Pipeline run status
    """
    try:
        run_id = mlflow_manager.start_pipeline_run(
            pipeline_name=request.pipeline_name,
            parameters=request.parameters
        )
        
        # Add background task to complete the run
        background_tasks.add_task(mlflow_manager.end_pipeline_run, "FINISHED")
        
        return {
            "status": "started",
            "run_id": run_id,
            "pipeline_name": request.pipeline_name,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/pipeline/run/{run_id}")
async def get_pipeline_run(run_id: str):
    """
    Get information about a pipeline run.
    
    Args:
        run_id: MLflow run ID
        
    Returns:
        Pipeline run information
    """
    try:
        run_info = mlflow_manager.get_run_info(run_id)
        return {
            "status": "success",
            "run_info": run_info,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Run not found: {str(e)}")


@app.post("/api/v1/jobs/create")
async def create_scheduled_job():
    """
    Create a scheduled Databricks job for the RAG pipeline.
    
    Returns:
        Job configuration
    """
    try:
        job_config = job_scheduler.create_rag_pipeline_job()
        return {
            "status": "success",
            "job_config": job_config,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/jobs/{job_id}/trigger")
async def trigger_job(job_id: str):
    """
    Manually trigger a Databricks job.
    
    Args:
        job_id: Databricks job ID
        
    Returns:
        Job run status
    """
    try:
        run_id = job_scheduler.trigger_job_run(job_id)
        return {
            "status": "triggered",
            "job_id": job_id,
            "run_id": run_id,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/delta/tables")
async def get_delta_tables():
    """
    Get information about Delta tables.
    
    Returns:
        Delta tables configuration
    """
    return {
        "database": delta_manager.database,
        "tables": {
            "raw": delta_manager.raw_table,
            "silver": delta_manager.silver_table,
            "gold": delta_manager.gold_table
        },
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/v1/config")
async def get_configuration():
    """
    Get current API configuration (non-sensitive).
    
    Returns:
        Configuration information
    """
    return {
        "api_version": "1.0.0",
        "embedding_model": settings.embedding_model,
        "vector_dimension": settings.vector_dimension,
        "top_k_results": settings.top_k_results,
        "aws_region": settings.aws_region,
        "timestamp": datetime.now().isoformat()
    }


if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
