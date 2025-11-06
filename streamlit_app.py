"""
Streamlit Frontend for Enterprise AI Agent Framework.
"""
import streamlit as st
import httpx
from datetime import datetime
from typing import Optional
import json

from config import settings


# Configure Streamlit page
st.set_page_config(
    page_title="Enterprise AI Agent Framework",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API endpoint
API_BASE_URL = f"http://{settings.api_host}:{settings.api_port}"


def make_api_request(endpoint: str, method: str = "GET", data: Optional[dict] = None):
    """Make HTTP request to the API."""
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = httpx.get(url, timeout=30.0)
        elif method == "POST":
            response = httpx.post(url, json=data, timeout=30.0)
        
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        st.error(f"API request failed: {str(e)}")
        return None


def main():
    """Main Streamlit application."""
    
    # Sidebar
    with st.sidebar:
        st.title("🤖 AI Agent Framework")
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Navigate",
            ["🏠 Home", "💬 RAG Query", "📊 Pipeline Status", "⚙️ Configuration"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### System Info")
        
        # Health check
        health = make_api_request("/health")
        if health:
            st.success(f"Status: {health.get('status', 'Unknown')}")
            st.caption(f"Version: {health.get('version', 'N/A')}")
    
    # Main content area
    if page == "🏠 Home":
        show_home_page()
    elif page == "💬 RAG Query":
        show_rag_query_page()
    elif page == "📊 Pipeline Status":
        show_pipeline_status_page()
    elif page == "⚙️ Configuration":
        show_configuration_page()


def show_home_page():
    """Display home page with architecture overview."""
    st.title("Enterprise AI Agent Framework")
    st.markdown("### RAG-based AI Agent with Databricks Lakehouse and AWS Bedrock")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏗️ Core Architecture")
        st.markdown("""
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
        """)
    
    with col2:
        st.markdown("#### ✨ Key Features")
        st.markdown("""
        - **Retrieval-Augmented Generation (RAG)** with LangChain
        - **Sentence-BERT Embeddings** for semantic search
        - **Databricks Vector Search** for efficient retrieval
        - **AWS Bedrock** for LLM inference (Claude/Titan)
        - **Delta Lake** medallion architecture (Raw → Silver → Gold)
        - **MLflow** for experiment tracking and pipeline management
        - **Databricks Jobs** for automated workflow scheduling
        """)
    
    st.markdown("---")
    
    # Quick stats
    st.markdown("#### 📈 Quick Stats")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("API Status", "Online", delta="Healthy")
    
    with col2:
        st.metric("Embedding Model", "Sentence-BERT", delta=None)
    
    with col3:
        st.metric("Vector Dimension", settings.vector_dimension, delta=None)
    
    with col4:
        st.metric("Top-K Results", settings.top_k_results, delta=None)


def show_rag_query_page():
    """Display RAG query interface."""
    st.title("💬 RAG Query Interface")
    st.markdown("Ask questions and get AI-powered answers with retrieved context")
    
    st.markdown("---")
    
    # Query input
    question = st.text_area(
        "Enter your question:",
        height=100,
        placeholder="What is the Enterprise AI Agent Framework?"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        context_length = st.number_input(
            "Context Documents",
            min_value=1,
            max_value=10,
            value=5,
            help="Number of documents to retrieve for context"
        )
    
    with col2:
        submit_button = st.button("🚀 Submit Query", type="primary", use_container_width=True)
    
    if submit_button and question:
        with st.spinner("Processing query..."):
            response = make_api_request(
                "/api/v1/query",
                method="POST",
                data={"question": question, "context_length": context_length}
            )
            
            if response:
                st.markdown("---")
                st.markdown("### 📝 Answer")
                st.info(response.get("answer", "No answer generated"))
                
                st.markdown("---")
                st.markdown("### 📚 Retrieved Context Documents")
                
                context_docs = response.get("context_documents", [])
                for i, doc in enumerate(context_docs, 1):
                    with st.expander(f"Document {i} - Score: {doc.get('metadata', {}).get('score', 'N/A')}"):
                        st.text(doc.get("content", "No content"))
                        st.caption(f"Source: {doc.get('metadata', {}).get('source', 'Unknown')}")
                
                st.success(f"Retrieved {response.get('num_documents_retrieved', 0)} documents")


def show_pipeline_status_page():
    """Display pipeline status and controls."""
    st.title("📊 Pipeline Status & Management")
    st.markdown("Monitor and control data pipelines and jobs")
    
    st.markdown("---")
    
    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["🔄 Pipeline Runs", "📋 Delta Tables", "⏰ Scheduled Jobs"])
    
    with tab1:
        st.markdown("#### MLflow Pipeline Runs")
        
        col1, col2 = st.columns(2)
        
        with col1:
            pipeline_name = st.text_input("Pipeline Name", value="rag_data_pipeline")
        
        with col2:
            if st.button("▶️ Start Pipeline Run", use_container_width=True):
                with st.spinner("Starting pipeline..."):
                    response = make_api_request(
                        "/api/v1/pipeline/run",
                        method="POST",
                        data={"pipeline_name": pipeline_name, "parameters": {}}
                    )
                    
                    if response:
                        st.success(f"Pipeline started! Run ID: {response.get('run_id')}")
        
        st.markdown("---")
        
        # Run ID lookup
        run_id = st.text_input("Enter Run ID to view details:")
        if run_id and st.button("🔍 Get Run Info"):
            response = make_api_request(f"/api/v1/pipeline/run/{run_id}")
            if response:
                st.json(response)
    
    with tab2:
        st.markdown("#### Delta Lake Tables")
        
        response = make_api_request("/api/v1/delta/tables")
        if response:
            st.markdown(f"**Database:** `{response.get('database')}`")
            
            tables = response.get("tables", {})
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Raw Table", tables.get("raw", "N/A"))
            
            with col2:
                st.metric("Silver Table", tables.get("silver", "N/A"))
            
            with col3:
                st.metric("Gold Table", tables.get("gold", "N/A"))
        
        st.markdown("---")
        st.markdown("#### Data Ingestion")
        
        uploaded_file = st.file_uploader("Upload documents (JSON)", type=["json"])
        if uploaded_file and st.button("📥 Ingest Documents"):
            try:
                documents = json.load(uploaded_file)
                response = make_api_request(
                    "/api/v1/ingest",
                    method="POST",
                    data={"documents": documents, "source": "upload"}
                )
                if response:
                    st.success(response.get("message", "Documents ingested"))
            except Exception as e:
                st.error(f"Error ingesting documents: {str(e)}")
    
    with tab3:
        st.markdown("#### Databricks Scheduled Jobs")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("➕ Create RAG Pipeline Job", use_container_width=True):
                response = make_api_request("/api/v1/jobs/create", method="POST")
                if response:
                    st.success("Job created successfully!")
                    st.json(response.get("job_config"))
        
        with col2:
            job_id = st.text_input("Job ID")
            if job_id and st.button("▶️ Trigger Job", use_container_width=True):
                response = make_api_request(
                    f"/api/v1/jobs/{job_id}/trigger",
                    method="POST"
                )
                if response:
                    st.success(f"Job triggered! Run ID: {response.get('run_id')}")


def show_configuration_page():
    """Display configuration information."""
    st.title("⚙️ Configuration")
    st.markdown("System configuration and settings")
    
    st.markdown("---")
    
    response = make_api_request("/api/v1/config")
    
    if response:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### General Settings")
            st.info(f"**API Version:** {response.get('api_version')}")
            st.info(f"**AWS Region:** {response.get('aws_region')}")
            st.info(f"**Embedding Model:** {response.get('embedding_model')}")
        
        with col2:
            st.markdown("#### Vector Search Settings")
            st.info(f"**Vector Dimension:** {response.get('vector_dimension')}")
            st.info(f"**Top-K Results:** {response.get('top_k_results')}")
            st.info(f"**Timestamp:** {response.get('timestamp')}")
    
    st.markdown("---")
    
    st.markdown("#### Environment Configuration")
    st.markdown("""
    The system uses environment variables for configuration. 
    Create a `.env` file based on `.env.example` with your credentials:
    
    - AWS credentials for Bedrock
    - Databricks workspace token
    - MLflow tracking URI
    - Delta Lake database settings
    """)
    
    with st.expander("📄 View .env.example"):
        try:
            with open(".env.example", "r") as f:
                st.code(f.read(), language="bash")
        except FileNotFoundError:
            st.warning(".env.example file not found")


if __name__ == "__main__":
    main()
