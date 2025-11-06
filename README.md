# Enterprise AI Agent Framework (MVP)

**Stack:** FastAPI + LangChain (RAG) + AWS Bedrock + Databricks (Delta + Vector Search) + Streamlit + Docker + GitHub Actions (CI/CD)

## Quickstart (Local)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # fill your Bedrock & Databricks values
uvicorn app.api.main:app --reload --port 8080
# In another shell:
streamlit run app/web/app.py
```

## API
- `GET /health`
- `POST /rag/query`  body: `{ "query": "your question" }`

## Structure
```
app/
  api/            # FastAPI API (RAG endpoint)
  web/            # Streamlit UI
  docker/         # Dockerfile & entrypoint
databricks/
  notebooks/      # Ingest, Chunk, Embed, Index
.github/workflows # CI (lint/test) + CD (ECR/ECS) + Databricks Job trigger
```

## Deploy (Docker)

```bash
docker build -t ai-agent:local -f app/docker/Dockerfile .
docker run -p 8080:8080 --env-file .env ai-agent:local
```

## Notes
- Replace placeholders with your Databricks Vector Search & Bedrock credentials.
- This is an MVP; add LangSmith / OpenTelemetry later.
