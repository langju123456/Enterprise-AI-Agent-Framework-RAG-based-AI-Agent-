# Deployment Guide

This guide provides instructions for deploying the Enterprise AI Agent Framework.

## Table of Contents
1. [Local Deployment](#local-deployment)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Databricks Configuration](#databricks-configuration)
5. [AWS Bedrock Setup](#aws-bedrock-setup)

## Local Deployment

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Access to AWS Bedrock (optional)
- Databricks workspace (optional)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/langju123456/nterprise-AI-Agent-Framework-RAG-based-AI-Agent-.git
   cd nterprise-AI-Agent-Framework-RAG-based-AI-Agent-
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

5. **Start services**
   ```bash
   # Start API
   python api.py

   # In a new terminal, start Streamlit
   streamlit run streamlit_app.py
   ```

6. **Access the application**
   - Streamlit UI: http://localhost:8501
   - API Documentation: http://localhost:8000/docs

## Docker Deployment

### Prerequisites
- Docker installed
- Docker Compose installed

### Steps

1. **Build and start containers**
   ```bash
   docker-compose up -d
   ```

2. **View logs**
   ```bash
   docker-compose logs -f
   ```

3. **Stop containers**
   ```bash
   docker-compose down
   ```

### Individual Container Commands

Build the image:
```bash
docker build -t rag-agent .
```

Run API container:
```bash
docker run -d -p 8000:8000 --env-file .env rag-agent python api.py
```

Run Streamlit container:
```bash
docker run -d -p 8501:8501 --env-file .env rag-agent streamlit run streamlit_app.py
```

## Cloud Deployment

### AWS Deployment

#### Using EC2

1. **Launch EC2 instance**
   - AMI: Ubuntu 22.04
   - Instance type: t3.medium or larger
   - Storage: 30GB+

2. **Connect and setup**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   
   # Install Docker
   sudo apt update
   sudo apt install -y docker.io docker-compose
   sudo usermod -aG docker ubuntu
   ```

3. **Deploy application**
   ```bash
   git clone your-repo-url
   cd nterprise-AI-Agent-Framework-RAG-based-AI-Agent-
   cp .env.example .env
   # Edit .env with credentials
   docker-compose up -d
   ```

4. **Configure security group**
   - Allow inbound: 8000 (API), 8501 (Streamlit)
   - Source: Your IP or 0.0.0.0/0 (for public access)

#### Using ECS (Elastic Container Service)

1. **Push to ECR**
   ```bash
   aws ecr create-repository --repository-name rag-agent
   docker tag rag-agent:latest <account-id>.dkr.ecr.<region>.amazonaws.com/rag-agent:latest
   docker push <account-id>.dkr.ecr.<region>.amazonaws.com/rag-agent:latest
   ```

2. **Create ECS task definition**
   - Use the provided Docker image
   - Configure environment variables
   - Set up port mappings (8000, 8501)

3. **Create ECS service**
   - Use Fargate or EC2 launch type
   - Configure load balancer
   - Set desired task count

### Azure Deployment

#### Using Azure Container Instances

```bash
az container create \
  --resource-group rag-agent-rg \
  --name rag-api \
  --image your-registry/rag-agent:latest \
  --ports 8000 8501 \
  --environment-variables $(cat .env)
```

### GCP Deployment

#### Using Cloud Run

```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/your-project/rag-agent

# Deploy to Cloud Run
gcloud run deploy rag-api \
  --image gcr.io/your-project/rag-agent \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Databricks Configuration

### Workspace Setup

1. **Create Databricks workspace**
   - Sign up at databricks.com or use cloud provider marketplace

2. **Generate access token**
   - User Settings → Access Tokens → Generate New Token
   - Save token securely

3. **Configure in .env**
   ```bash
   DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
   DATABRICKS_TOKEN=your_token_here
   ```

### Create Delta Tables

1. **Import notebooks**
   - Upload notebooks from `databricks_workflows/` directory
   - Place in `/Workflows/` folder

2. **Run setup notebook**
   ```python
   # Run 01_ingest_data.py to create tables
   ```

### Setup Vector Search

1. **Enable Vector Search**
   - Go to Compute → Vector Search
   - Create endpoint

2. **Create index**
   ```python
   from databricks.vector_search.client import VectorSearchClient
   
   client = VectorSearchClient()
   client.create_index(
       index_name="rag_vector_index",
       endpoint_name="your_endpoint",
       primary_key="id",
       embedding_dimension=384,
       embedding_vector_column="embedding_vector"
   )
   ```

### Schedule Jobs

1. **Create job from API**
   - Use `/api/v1/jobs/create` endpoint
   - Or manually in Databricks UI

2. **Configure schedule**
   - Workflows → Jobs → Create Job
   - Add tasks from notebooks
   - Set schedule (e.g., daily at 2 AM)

## AWS Bedrock Setup

### Prerequisites
- AWS account with Bedrock access
- Bedrock model access requested

### Steps

1. **Request model access**
   - AWS Console → Bedrock → Model access
   - Request access to Claude or Titan models
   - Wait for approval (usually instant)

2. **Create IAM user**
   ```bash
   aws iam create-user --user-name rag-bedrock-user
   ```

3. **Attach policy**
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "bedrock:InvokeModel",
           "bedrock:InvokeModelWithResponseStream"
         ],
         "Resource": "*"
       }
     ]
   }
   ```

4. **Generate access keys**
   ```bash
   aws iam create-access-key --user-name rag-bedrock-user
   ```

5. **Configure in .env**
   ```bash
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_REGION=us-east-1
   AWS_BEDROCK_MODEL=anthropic.claude-v2
   ```

## Production Considerations

### Security
- Use secrets manager (AWS Secrets Manager, Azure Key Vault)
- Enable HTTPS with SSL certificates
- Implement API authentication (OAuth, API keys)
- Use VPC/private networking

### Monitoring
- Set up CloudWatch/Azure Monitor/Stackdriver
- Configure alerts for API errors
- Monitor Bedrock usage and costs
- Track MLflow experiments

### Scaling
- Use auto-scaling for containers
- Implement API rate limiting
- Cache frequently accessed data
- Use CDN for static assets

### Backup
- Regular Delta Lake backups
- Export MLflow experiments
- Version control for notebooks
- Database snapshots

## Troubleshooting

### Common Issues

**Port already in use**
```bash
# Find process using port
lsof -i :8000
# Kill process
kill -9 <PID>
```

**Docker build fails**
```bash
# Clear Docker cache
docker system prune -a
# Rebuild
docker-compose build --no-cache
```

**Bedrock access denied**
- Verify model access is granted
- Check IAM permissions
- Ensure correct region

**Databricks connection failed**
- Verify token is valid
- Check workspace URL
- Ensure network connectivity

## Support

For issues and questions:
- GitHub Issues: [Repository Issues](https://github.com/langju123456/nterprise-AI-Agent-Framework-RAG-based-AI-Agent-/issues)
- Documentation: See README.md
