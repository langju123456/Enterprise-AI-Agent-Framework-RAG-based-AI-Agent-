# Enterprise AI Agent Framework - RAG-based AI Agent

Built an enterprise-grade AI agent framework integrating FastAPI, LangChain, and Databricks Lakehouse for scalable RAG workflows and automated cloud deployment.

## 🏗️ Core Architecture

```
[Streamlit Frontend]
       ↓
[FastAPI REST API]
   →  RAG Pipeline (LangChain)
        ├── Sentence-BERT Embeddings
        ├── Databricks Vector Search (Retriever)
        ├── AWS Bedrock Inference (Claude / Titan)
       ↓
[Databricks Lakehouse]
   - Delta Tables (Raw, Silver, Gold)
   - Jobs & MLflow (Pipeline Scheduling)
```

## ✨ Features

### RAG Pipeline
- **Retrieval-Augmented Generation** powered by LangChain
- **Sentence-BERT Embeddings** for semantic document similarity
- **Databricks Vector Search** for efficient document retrieval
- **AWS Bedrock** integration for LLM inference (Claude and Titan models)

### Data Architecture
- **Delta Lake Medallion Architecture**
  - **Raw Layer**: Ingested data as-is
  - **Silver Layer**: Cleaned and enriched data with embeddings
  - **Gold Layer**: Aggregated analytics-ready data
- **MLflow** for experiment tracking and model management
- **Databricks Jobs** for automated pipeline scheduling

### API & Frontend
- **FastAPI REST API** with comprehensive endpoints
- **Streamlit Web UI** for interactive queries and pipeline management
- **Real-time health monitoring** and configuration management

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- AWS account with Bedrock access
- Databricks workspace (optional for full functionality)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/langju123456/nterprise-AI-Agent-Framework-RAG-based-AI-Agent-.git
cd nterprise-AI-Agent-Framework-RAG-based-AI-Agent-
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your credentials
```

### Running the Application

#### Option 1: Start all services (Linux/Mac)
```bash
./start_services.sh
```

#### Option 2: Start services individually

Start the FastAPI server:
```bash
python api.py
```

Start the Streamlit frontend (in a new terminal):
```bash
streamlit run streamlit_app.py
```

### Access the Application

- **Streamlit UI**: http://localhost:8501
- **FastAPI Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

## 📚 API Endpoints

### Query Endpoints
- `POST /api/v1/query` - Execute RAG query
- `POST /api/v1/ingest` - Ingest documents

### Pipeline Management
- `POST /api/v1/pipeline/run` - Start pipeline run
- `GET /api/v1/pipeline/run/{run_id}` - Get pipeline run status

### Job Scheduling
- `POST /api/v1/jobs/create` - Create scheduled job
- `POST /api/v1/jobs/{job_id}/trigger` - Trigger job run

### Configuration
- `GET /api/v1/config` - Get configuration
- `GET /api/v1/delta/tables` - Get Delta tables info

## 🏗️ Project Structure

```
.
├── api.py                      # FastAPI REST API
├── streamlit_app.py           # Streamlit frontend
├── rag_pipeline.py            # RAG pipeline implementation
├── databricks_integration.py  # Databricks/MLflow integration
├── config.py                  # Configuration management
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── start_services.sh         # Service startup script
└── README.md                 # This file
```

## 🔧 Configuration

Key configuration options in `.env`:

### AWS Bedrock
```bash
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
AWS_BEDROCK_MODEL=anthropic.claude-v2
```

### Databricks
```bash
DATABRICKS_HOST=https://your-workspace.databricks.com
DATABRICKS_TOKEN=your_token
DATABRICKS_VECTOR_SEARCH_ENDPOINT=your_endpoint
```

### MLflow
```bash
MLFLOW_TRACKING_URI=databricks
MLFLOW_EXPERIMENT_NAME=/Users/your_user/rag_experiment
```

### Delta Lake
```bash
DELTA_TABLE_RAW=raw_data
DELTA_TABLE_SILVER=silver_data
DELTA_TABLE_GOLD=gold_data
DELTA_DATABASE=rag_database
```

## 🧪 Usage Examples

### Python API Client

```python
import httpx

# Query the RAG system
response = httpx.post(
    "http://localhost:8000/api/v1/query",
    json={
        "question": "What is the Enterprise AI Agent Framework?",
        "context_length": 5
    }
)
print(response.json())
```

### Using the Streamlit UI

1. Navigate to http://localhost:8501
2. Select "RAG Query" from the sidebar
3. Enter your question
4. View the AI-generated answer with retrieved context

## 🔄 Pipeline Workflow

1. **Data Ingestion** → Raw Delta Table
2. **Data Cleaning** → Silver Delta Table
3. **Embedding Generation** → Silver Table (with embeddings)
4. **Aggregation** → Gold Delta Table
5. **Vector Indexing** → Databricks Vector Search
6. **Query Processing** → RAG Pipeline → User

## 📊 Monitoring & Tracking

- **MLflow**: Track experiments, parameters, and metrics
- **Databricks Jobs**: Monitor scheduled pipeline runs
- **Health Endpoints**: Real-time API status monitoring
- **Streamlit Dashboard**: Visual pipeline status and configuration

## 🛠️ Development

### Adding New Features

1. **Custom Embeddings**: Modify `SentenceBERTEmbeddings` in `rag_pipeline.py`
2. **New API Endpoints**: Add to `api.py`
3. **UI Components**: Extend `streamlit_app.py`
4. **Pipeline Steps**: Update `databricks_integration.py`

## 🔐 Security Notes

- Never commit `.env` file with credentials
- Use environment variables for all sensitive data
- Implement proper authentication in production
- Enable HTTPS for production deployments

## 📝 License

See LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.
