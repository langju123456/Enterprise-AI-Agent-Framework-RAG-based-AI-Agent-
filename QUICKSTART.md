# Quick Start Guide

Get the Enterprise AI Agent Framework up and running in minutes.

## Prerequisites

- Python 3.9 or higher
- pip package manager
- Git

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/langju123456/Enterprise-AI-Agent-Framework-RAG-based-AI-Agent-.git
cd Enterprise-AI-Agent-Framework-RAG-based-AI-Agent-
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

**Minimum required configuration for local testing:**

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
STREAMLIT_PORT=8501

# Embedding Model (will download automatically)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

**For full functionality, also configure:**

```bash
# AWS Bedrock
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
AWS_BEDROCK_MODEL=anthropic.claude-v2

# Databricks
DATABRICKS_HOST=https://your-workspace.databricks.com
DATABRICKS_TOKEN=your_databricks_token
```

### 4. Start the Application

#### Option A: Using the start script (Linux/Mac)

```bash
./start_services.sh
```

#### Option B: Manual start

**Terminal 1 - Start the API:**
```bash
python api.py
```

**Terminal 2 - Start the UI:**
```bash
streamlit run streamlit_app.py
```

#### Option C: Using Docker

```bash
# Make sure .env is configured
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Access the Application

Once started, access these URLs in your browser:

- **Streamlit UI**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/health

## First Steps

### 1. Verify Installation

Visit http://localhost:8501 and check the sidebar shows:
- ✅ Status: healthy
- Version number displayed

### 2. Try a RAG Query

1. Click on "💬 RAG Query" in the sidebar
2. Enter a question, for example:
   ```
   What is the Enterprise AI Agent Framework?
   ```
3. Adjust "Context Documents" (1-10)
4. Click "🚀 Submit Query"
5. View the AI-generated answer and retrieved context

### 3. Explore the API

Visit http://localhost:8000/docs to see:
- Interactive API documentation
- All available endpoints
- Request/response schemas
- Try out the API directly

### 4. Test an API Endpoint

```bash
# Health check
curl http://localhost:8000/health

# Get configuration
curl http://localhost:8000/api/v1/config

# Submit a query
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is RAG?", "context_length": 5}'
```

## Testing Without Cloud Services

The framework is designed to work in development mode without AWS Bedrock or Databricks:

- **Embeddings**: Uses local Sentence-BERT model (downloads automatically)
- **Vector Search**: Uses simulated retrieval for testing
- **LLM**: Returns placeholder responses if Bedrock is not configured

### Running Basic Tests

```bash
python test_framework.py
```

This will verify:
- ✅ All modules import correctly
- ✅ Configuration loads properly
- ✅ Embeddings generate successfully
- ✅ RAG pipeline initializes
- ✅ API endpoints are defined

## Configuration Options

### Embedding Models

Change the embedding model in `.env`:

```bash
# Small and fast (384 dimensions)
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Better quality (768 dimensions)
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2

# Multilingual support (768 dimensions)
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

### API Configuration

```bash
# Change ports if 8000/8501 are in use
API_PORT=8080
STREAMLIT_PORT=8502

# Bind to specific interface
API_HOST=127.0.0.1  # localhost only
API_HOST=0.0.0.0    # all interfaces
```

### Vector Search

```bash
# Number of documents to retrieve
TOP_K_RESULTS=5

# Vector dimension (must match embedding model)
VECTOR_DIMENSION=384
```

## Common Issues

### Port Already in Use

```bash
# Find process using the port
lsof -i :8000
lsof -i :8501

# Kill the process
kill -9 <PID>

# Or use different ports in .env
```

### Module Not Found Errors

```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Or install specific missing package
pip install fastapi uvicorn streamlit
```

### Slow First Query

The first query will be slower because:
1. Sentence-BERT model needs to download (~100MB)
2. Model loads into memory
3. First inference initializes the model

Subsequent queries will be much faster.

### Docker Issues

```bash
# Rebuild containers
docker-compose build --no-cache

# Remove old containers
docker-compose down -v

# Start fresh
docker-compose up -d
```

## Next Steps

### 1. Set Up AWS Bedrock

1. Create AWS account
2. Request Bedrock model access (Claude or Titan)
3. Create IAM user with Bedrock permissions
4. Add credentials to `.env`
5. Test with a query

See [DEPLOYMENT.md](DEPLOYMENT.md#aws-bedrock-setup) for detailed instructions.

### 2. Set Up Databricks

1. Create Databricks workspace
2. Generate access token
3. Import notebooks from `databricks_workflows/`
4. Run initial data ingestion
5. Create scheduled jobs

See [DEPLOYMENT.md](DEPLOYMENT.md#databricks-configuration) for detailed instructions.

### 3. Ingest Your Own Data

**Via API:**
```bash
curl -X POST http://localhost:8000/api/v1/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      {
        "id": "doc1",
        "content": "Your document text here",
        "metadata": "{\"source\": \"custom\"}",
        "source": "api"
      }
    ],
    "source": "api"
  }'
```

**Via Databricks:**
Run the `01_ingest_data.py` notebook with your data.

### 4. Customize the RAG Pipeline

Edit `rag_pipeline.py` to:
- Change retrieval strategy
- Modify prompt templates
- Add pre/post-processing
- Implement custom filters

### 5. Deploy to Production

Follow [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Cloud deployment (AWS/Azure/GCP)
- Container orchestration
- Monitoring setup
- Security hardening

## Learning Resources

### Understanding RAG

- **What is RAG?**: Retrieval-Augmented Generation combines document retrieval with LLM generation
- **Why RAG?**: Provides up-to-date, factual responses grounded in your documents
- **How it works**: Query → Retrieve relevant docs → Augment prompt → Generate answer

### Project Documentation

- [README.md](README.md) - Project overview and features
- [ARCHITECTURE.md](ARCHITECTURE.md) - Detailed architecture documentation
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment guide

### API Documentation

Once running, visit:
- http://localhost:8000/docs - Interactive API docs
- http://localhost:8000/redoc - Alternative API documentation

## Getting Help

### Troubleshooting

1. Check the console logs for errors
2. Verify `.env` configuration
3. Ensure all dependencies are installed
4. Try restarting the services

### Support Channels

- **GitHub Issues**: Report bugs or request features
- **Documentation**: Check README, ARCHITECTURE, and DEPLOYMENT docs
- **API Docs**: Interactive documentation at `/docs` endpoint

## Quick Reference

### Important Files

```
├── api.py                     # FastAPI REST API
├── streamlit_app.py          # Streamlit frontend
├── rag_pipeline.py           # RAG implementation
├── databricks_integration.py # Databricks/MLflow
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
├── .env                      # Your configuration (create from .env.example)
└── start_services.sh         # Quick start script
```

### Key Commands

```bash
# Start services
./start_services.sh

# Run tests
python test_framework.py

# Start with Docker
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Important URLs

- UI: http://localhost:8501
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## Success Checklist

- [ ] Repository cloned
- [ ] Dependencies installed
- [ ] `.env` file created and configured
- [ ] Services started successfully
- [ ] Streamlit UI accessible
- [ ] API documentation accessible
- [ ] Health check returns "healthy"
- [ ] First RAG query submitted
- [ ] Response received with context

Congratulations! You're ready to build with the Enterprise AI Agent Framework! 🎉
