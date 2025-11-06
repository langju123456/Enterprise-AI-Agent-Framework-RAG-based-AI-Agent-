"""
Basic tests for the Enterprise AI Agent Framework.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported."""
    try:
        import config
        import rag_pipeline
        import databricks_integration
        import api
        print("✓ All modules imported successfully")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False


def test_config():
    """Test configuration loading."""
    try:
        from config import settings
        assert settings.api_port == 8000
        assert settings.embedding_model == "sentence-transformers/all-MiniLM-L6-v2"
        assert settings.vector_dimension == 384
        print("✓ Configuration loaded successfully")
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False


def test_embeddings():
    """Test embedding generation."""
    try:
        from rag_pipeline import SentenceBERTEmbeddings
        
        embeddings = SentenceBERTEmbeddings()
        test_text = "This is a test sentence."
        
        # Test single embedding
        embedding = embeddings.embed_query(test_text)
        assert isinstance(embedding, list)
        assert len(embedding) > 0
        
        # Test batch embeddings
        texts = ["First sentence.", "Second sentence."]
        batch_embeddings = embeddings.embed_documents(texts)
        assert len(batch_embeddings) == 2
        
        print(f"✓ Embeddings generated successfully (dimension: {len(embedding)})")
        return True
    except Exception as e:
        print(f"✗ Embeddings test failed: {e}")
        return False


def test_rag_pipeline():
    """Test RAG pipeline initialization."""
    try:
        from rag_pipeline import RAGPipeline
        
        pipeline = RAGPipeline()
        assert pipeline.embeddings is not None
        assert pipeline.retriever is not None
        assert pipeline.llm is not None
        
        print("✓ RAG pipeline initialized successfully")
        return True
    except Exception as e:
        print(f"✗ RAG pipeline test failed: {e}")
        return False


def test_delta_manager():
    """Test Delta table manager."""
    try:
        from databricks_integration import DeltaTableManager
        
        manager = DeltaTableManager()
        assert manager.database == "rag_database"
        assert manager.raw_table.endswith("raw_data")
        assert manager.silver_table.endswith("silver_data")
        assert manager.gold_table.endswith("gold_data")
        
        print("✓ Delta table manager initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Delta manager test failed: {e}")
        return False


def test_mlflow_manager():
    """Test MLflow pipeline manager."""
    try:
        from databricks_integration import MLflowPipelineManager
        
        # Note: This may fail if MLflow tracking URI is not accessible
        # but we're just testing initialization
        manager = MLflowPipelineManager()
        print("✓ MLflow manager initialized successfully")
        return True
    except Exception as e:
        print(f"✗ MLflow manager test failed: {e}")
        return False


def test_api_endpoints():
    """Test API endpoint definitions."""
    try:
        from api import app
        
        # Get all routes
        routes = [route.path for route in app.routes]
        
        # Check key endpoints exist
        assert "/" in routes
        assert "/health" in routes
        assert "/api/v1/query" in routes
        assert "/api/v1/config" in routes
        
        print(f"✓ API has {len(routes)} endpoints defined")
        return True
    except Exception as e:
        print(f"✗ API test failed: {e}")
        return False


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Running Enterprise AI Agent Framework Tests")
    print("=" * 60)
    print()
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration", test_config),
        ("Embeddings", test_embeddings),
        ("RAG Pipeline", test_rag_pipeline),
        ("Delta Manager", test_delta_manager),
        ("MLflow Manager", test_mlflow_manager),
        ("API Endpoints", test_api_endpoints),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\nTest: {test_name}")
        print("-" * 60)
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test crashed: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
