# Enterprise AI Agent Framework - Architecture

## System Architecture Overview

This document describes the architecture of the Enterprise AI Agent Framework, a RAG-based AI agent system integrating FastAPI, LangChain, Databricks Lakehouse, and AWS Bedrock.

## Architecture Layers

### 1. Presentation Layer - Streamlit Frontend

**File**: `streamlit_app.py`

The Streamlit frontend provides an interactive web interface for users to:
- Submit RAG queries
- View AI-generated responses with context
- Monitor pipeline status
- Manage Databricks jobs
- Ingest documents
- View system configuration

**Key Features**:
- Real-time health monitoring
- Multi-page navigation (Home, RAG Query, Pipeline Status, Configuration)
- File upload for document ingestion
- Interactive query interface with adjustable context length
- Visual display of retrieved context documents

### 2. API Layer - FastAPI REST API

**File**: `api.py`

The FastAPI layer exposes RESTful endpoints for:
- RAG query processing
- Document ingestion
- Pipeline management
- Job scheduling
- Configuration retrieval

**Endpoints**:
- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /api/v1/query` - Execute RAG query
- `POST /api/v1/ingest` - Ingest documents
- `POST /api/v1/pipeline/run` - Start pipeline run
- `GET /api/v1/pipeline/run/{run_id}` - Get run status
- `POST /api/v1/jobs/create` - Create scheduled job
- `POST /api/v1/jobs/{job_id}/trigger` - Trigger job
- `GET /api/v1/delta/tables` - Get Delta tables info
- `GET /api/v1/config` - Get configuration

### 3. RAG Pipeline Layer

**File**: `rag_pipeline.py`

The RAG pipeline orchestrates the Retrieval-Augmented Generation workflow:

#### Components:

**a) SentenceBERTEmbeddings**
- Implements LangChain Embeddings interface
- Uses Sentence-BERT transformer models
- Default model: `sentence-transformers/all-MiniLM-L6-v2`
- Vector dimension: 384
- Methods:
  - `embed_documents()` - Batch document embedding
  - `embed_query()` - Single query embedding

**b) DatabricksVectorSearchRetriever**
- Integrates with Databricks Vector Search
- Retrieves top-k relevant documents
- Returns LangChain Document objects with metadata
- Configurable similarity threshold

**c) AWSBedrockInference**
- Interfaces with AWS Bedrock for LLM inference
- Supports Claude and Titan models
- Configurable parameters:
  - `max_tokens`: Maximum generation length
  - `temperature`: Sampling temperature
  - `top_p`: Nucleus sampling parameter

**d) RAGPipeline**
- Main orchestration class
- End-to-end query processing:
  1. Embed query with SentenceBERT
  2. Retrieve relevant documents from Vector Search
  3. Build augmented prompt with context
  4. Generate answer using Bedrock LLM
  5. Return structured response with metadata

### 4. Data Layer - Databricks Lakehouse

**File**: `databricks_integration.py`

#### Delta Lake Medallion Architecture

**a) Raw Layer** (`DeltaTableManager.raw_table`)
- Ingests raw data as-is
- Schema:
  - `id`: Document identifier
  - `content`: Raw text content
  - `metadata`: JSON metadata
  - `source`: Data source identifier
  - `ingestion_timestamp`: Ingestion time
- Partitioned by: `source`

**b) Silver Layer** (`DeltaTableManager.silver_table`)
- Cleaned and enriched data
- Schema:
  - `id`: Document identifier
  - `content`: Cleaned text content
  - `embeddings`: Vector embeddings (ARRAY<FLOAT>)
  - `metadata`: JSON metadata
  - `source`: Data source
  - `processing_timestamp`: Processing time
  - `quality_score`: Data quality metric
- Partitioned by: `source`

**c) Gold Layer** (`DeltaTableManager.gold_table`)
- Analytics-ready aggregated data
- Schema:
  - `id`: Document identifier
  - `aggregated_content`: Processed content
  - `topic`: Document topic/category
  - `category`: Document category
  - `embedding_vector`: Final embeddings
  - `metadata`: JSON metadata
  - `creation_timestamp`: Creation time
  - `usage_count`: Query usage counter
- Partitioned by: `topic`

#### MLflow Pipeline Management

**MLflowPipelineManager** provides:
- Experiment tracking
- Parameter logging
- Metric logging
- Artifact storage
- Run management

**Key Methods**:
- `start_pipeline_run()` - Initialize MLflow run
- `log_pipeline_metrics()` - Log performance metrics
- `log_pipeline_artifacts()` - Save artifacts
- `end_pipeline_run()` - Finalize run
- `get_run_info()` - Retrieve run details

#### Databricks Job Scheduling

**DatabricksJobScheduler** manages:
- Automated pipeline execution
- Task dependencies
- Cron-based scheduling
- Job monitoring

**Pipeline Tasks**:
1. **ingest_raw_data** - Load data to Raw layer
2. **process_to_silver** - Clean and transform to Silver
3. **generate_embeddings** - Create vector embeddings
4. **promote_to_gold** - Aggregate to Gold layer

**Default Schedule**: Daily at 2 AM UTC

### 5. Configuration Management

**File**: `config.py`

Centralized configuration using Pydantic Settings:
- Environment variable loading
- Type validation
- Default values
- Sensitive data protection

**Configuration Groups**:
- AWS Bedrock settings
- Databricks workspace settings
- MLflow tracking settings
- Delta Lake table names
- Application settings
- Embedding model settings
- Vector search settings

## Data Flow

### Query Processing Flow

```
User Input (Streamlit)
    ↓
HTTP POST /api/v1/query
    ↓
RAGPipeline.query()
    ↓
┌─────────────────────────────────┐
│ 1. Embed Query                  │
│    SentenceBERTEmbeddings       │
│    → 384-dim vector             │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ 2. Retrieve Context             │
│    DatabricksVectorSearch       │
│    → Top-K documents            │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ 3. Build Augmented Prompt       │
│    Context + User Question      │
└─────────────────────────────────┘
    ↓
┌─────────────────────────────────┐
│ 4. Generate Answer              │
│    AWS Bedrock (Claude/Titan)   │
│    → AI Response                │
└─────────────────────────────────┘
    ↓
Response with Answer + Context
    ↓
Display in Streamlit UI
```

### Data Ingestion Flow

```
Source Data
    ↓
Raw Delta Table
    ↓
Data Cleaning & Validation
    ↓
Silver Delta Table
    ↓
Embedding Generation (SentenceBERT)
    ↓
Silver Table Updated with Embeddings
    ↓
Aggregation & Topic Classification
    ↓
Gold Delta Table
    ↓
Vector Index Creation
    ↓
Databricks Vector Search
    ↓
Ready for RAG Queries
```

## Workflow Automation

### Databricks Notebooks

Located in `databricks_workflows/`:

1. **01_ingest_data.py**
   - Creates database and Raw table
   - Ingests sample/source data
   - Validates ingestion

2. **02_process_silver.py**
   - Creates Silver table
   - Cleans and transforms data
   - Filters duplicate records

3. **03_generate_embeddings.py**
   - Loads SentenceBERT model
   - Generates embeddings in batches
   - Updates Silver table via MERGE

4. **04_promote_gold.py**
   - Creates Gold table
   - Aggregates and categorizes data
   - Generates pipeline summary

### Scheduled Execution

Jobs created via `DatabricksJobScheduler`:
- Task dependency graph
- Automatic retries
- Email notifications on failure
- Configurable concurrency

## Deployment Architecture

### Local Development

```
┌─────────────────────────────────┐
│   Developer Workstation         │
│                                 │
│  ┌──────────┐   ┌──────────┐  │
│  │ FastAPI  │   │Streamlit │  │
│  │  :8000   │   │  :8501   │  │
│  └──────────┘   └──────────┘  │
│                                 │
│  ┌──────────────────────────┐  │
│  │  Local Environment       │  │
│  │  (.env configuration)    │  │
│  └──────────────────────────┘  │
└─────────────────────────────────┘
         ↓
    Internet
         ↓
┌─────────────────┐ ┌─────────────┐
│  AWS Bedrock    │ │ Databricks  │
│  (LLM API)      │ │ Workspace   │
└─────────────────┘ └─────────────┘
```

### Docker Deployment

```
┌──────────────────────────────────┐
│   Docker Compose Environment     │
│                                  │
│  ┌────────────┐  ┌────────────┐ │
│  │ API        │  │ Frontend   │ │
│  │ Container  │  │ Container  │ │
│  │ :8000      │  │ :8501      │ │
│  └────────────┘  └────────────┘ │
│         │              │         │
│         └──────┬───────┘         │
│                │                 │
│         ┌──────┴──────┐          │
│         │  rag-network│          │
│         └─────────────┘          │
└──────────────────────────────────┘
```

### Cloud Production

```
┌───────────────────────────────────────┐
│   Cloud Infrastructure                │
│                                       │
│  ┌─────────────────────────────────┐ │
│  │  Load Balancer                  │ │
│  └──────────┬──────────────────────┘ │
│             │                         │
│  ┌──────────┴──────────┐             │
│  │  Container Service  │             │
│  │  (ECS/AKS/GKE)      │             │
│  │  ┌────┐  ┌────┐    │             │
│  │  │API │  │ UI │    │             │
│  │  └────┘  └────┘    │             │
│  └─────────────────────┘             │
└───────────────────────────────────────┘
         │              │
         ↓              ↓
┌─────────────┐  ┌──────────────────┐
│AWS Bedrock  │  │  Databricks      │
│  - Claude   │  │  - Delta Tables  │
│  - Titan    │  │  - Vector Search │
│             │  │  - MLflow        │
└─────────────┘  └──────────────────┘
```

## Security Considerations

### Environment Variables
- All credentials in `.env` file
- `.env` excluded from version control
- `.env.example` as template

### API Security
- CORS middleware configured
- Input validation via Pydantic
- Error handling without info leakage
- Rate limiting (recommended for production)

### Cloud Security
- IAM roles for AWS Bedrock access
- Databricks token authentication
- Network security groups
- HTTPS/TLS encryption

## Performance Optimization

### Caching
- Model caching (SentenceBERT loaded once)
- Connection pooling for databases
- API response caching (recommended)

### Parallel Processing
- Batch embedding generation
- Async API endpoints
- Spark parallel processing in Databricks

### Scalability
- Stateless API design
- Horizontal scaling via containers
- Delta Lake for large datasets
- Vector search indexing

## Monitoring and Observability

### Health Checks
- API health endpoint (`/health`)
- Streamlit real-time status

### Logging
- MLflow experiment tracking
- Pipeline run metrics
- API request/response logs

### Metrics
- Query latency
- Embedding generation time
- Retrieval accuracy
- LLM token usage
- Pipeline execution time

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Frontend | Streamlit | Interactive web UI |
| API | FastAPI | REST API service |
| Orchestration | LangChain | RAG pipeline framework |
| Embeddings | Sentence-BERT | Semantic embeddings |
| Vector Search | Databricks Vector Search | Document retrieval |
| LLM | AWS Bedrock | Text generation |
| Data Lake | Delta Lake | ACID-compliant storage |
| Orchestration | Databricks Jobs | Workflow automation |
| Tracking | MLflow | Experiment management |
| Containerization | Docker | Deployment packaging |

## Future Enhancements

### Planned Features
1. User authentication and authorization
2. Query result caching
3. Advanced vector search filters
4. Custom embedding models
5. Multi-modal support (images, PDFs)
6. Real-time data ingestion
7. A/B testing for prompts
8. Fine-tuned models in MLflow

### Scalability Improvements
1. Redis caching layer
2. Kubernetes deployment
3. CDN for static assets
4. Database read replicas
5. Async job processing with Celery

## Conclusion

This architecture provides a robust, scalable foundation for enterprise-grade RAG applications. The modular design allows for easy customization and extension while maintaining production-ready reliability.
