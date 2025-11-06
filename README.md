<h1 align="center">🤖 Enterprise AI Agent Framework</h1>
<p align="center">
  <em>Created by <strong>Lang Ju</strong> — AI Engineer & Product Builder</em><br/>
  <a href="https://github.com/langju"><img src="https://img.shields.io/badge/GitHub-langju-black?logo=github" /></a>
  <a href="mailto:ju.l@wustl.edu"><img src="https://img.shields.io/badge/Email-ju.l@wustl.edu-red?logo=gmail" /></a>
</p>

---

### 🧭 Introduction
**Enterprise AI Agent Framework** is a full-stack intelligent system designed for scalable enterprise applications.  
It combines **FastAPI**, **LangChain**, **Databricks Lakehouse**, and **AWS Bedrock** to enable secure and efficient Retrieval-Augmented Generation (RAG) pipelines — from data ingestion to deployment.

> A project that bridges applied AI engineering, cloud deployment, and modern MLOps practices.

---

### ⚙️ System Overview

<p align="center">
  <img src="assets/architecture.png" width="720"/>
</p>

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

---

### 🧩 Core Components

| Layer | Technologies | Description |
|--------|--------------|--------------|
| **Frontend** | Streamlit | Interactive UI for input and visualization |
| **Backend** | FastAPI + LangChain | Core API with modular RAG logic |
| **Embeddings** | Sentence-BERT | Text embeddings for semantic search |
| **Data & Vector Store** | Databricks Delta Lake + Vector Search | Knowledge management and retrieval |
| **Model Inference** | AWS Bedrock (Claude / Titan) | Secure enterprise LLM endpoint |
| **CI/CD Pipeline** | GitHub Actions + Docker + ECS | Continuous testing, build, and deployment |
| **Monitoring** | CloudWatch + LangSmith (optional) | Performance, latency, and logging insights |

---

### 🔁 Workflow

<p align="center">
  <img src="assets/workflow.png" width="720"/>
</p>

1. **Data Ingestion** → Clean and import documents into Databricks Delta Lake.  
2. **Chunking & Embedding** → Generate Sentence-BERT vectors for semantic representation.  
3. **Vector Indexing** → Build searchable indexes using Databricks Vector Search.  
4. **Query Execution** → FastAPI routes handle user queries through LangChain.  
5. **Context Retrieval & Generation** → Retrieve top results and query AWS Bedrock for contextual answers.  
6. **User Interaction** → Streamlit displays generated answers and context sources.  
7. **Observability** → Monitor requests and performance metrics via CloudWatch.  

---

### 🚀 Key Features

- **End-to-End RAG Pipeline:** from document ingestion to semantic retrieval and LLM response.  
- **Databricks Integration:** Delta + Vector Search for real-time retrieval.  
- **Cloud-Native Deployment:** Dockerized backend deployed to AWS ECS.  
- **Automated CI/CD:** GitHub Actions pipeline for build, test, and deployment.  
- **Observability Ready:** CloudWatch logging and LangSmith compatibility.  
- **Scalable Architecture:** Modular design, extendable to LangGraph multi-agent workflows.  

---

### 🧰 Tech Stack Summary

| Category | Stack |
|-----------|--------|
| **Backend** | FastAPI · LangChain · AWS Bedrock |
| **Data Layer** | Databricks · Delta Lake · Vector Search |
| **Embeddings** | Sentence-BERT |
| **Frontend** | Streamlit |
| **CI/CD & MLOps** | GitHub Actions · Docker · ECS · MLflow |
| **Monitoring** | CloudWatch · LangSmith-ready |
| **Version Control** | Git · DVC (optional) |

---

### 🧠 Quickstart

```bash
# Clone and setup
git clone https://github.com/langju/enterprise-ai-agent-framework.git
cd enterprise-ai-agent-framework
pip install -r requirements.txt
cp .env.example .env

# Run services
uvicorn app.api.main:app --reload
streamlit run app/web/app.py
```

---

### 🖥️ Demo

<p align="center">
  <img src="assets/demo.png" width="720"/>
</p>

> Replace with your Streamlit Cloud demo link or architecture screenshots.

---

### 📊 Professional Highlights

| Focus Area | Keywords |
|-------------|-----------|
| **Core Technologies** | FastAPI · LangChain · Databricks · Delta Lake · AWS Bedrock · Docker · CI/CD · Streamlit |
| **MLOps Expertise** | Version Control · Automated Deployment · Cloud Observability · MLflow Tracking |
| **System Architecture** | End-to-End AI System Design · Cloud-Native · Modular Workflow |
| **Future Roadmap** | LangGraph Multi-Agent Framework · OpenTelemetry Tracing |

---

<p align="center">
  <em>✨ Built with precision and vision by <strong>Lang Ju</strong> — bridging AI architecture and intelligent automation. ✨</em>
</p>
