"""
RAG Pipeline implementation with LangChain, Sentence-BERT, and AWS Bedrock.
"""
from typing import List, Dict, Any, Optional
from langchain.embeddings.base import Embeddings
from langchain.schema import Document
from sentence_transformers import SentenceTransformer
import boto3
import json
from config import settings


class SentenceBERTEmbeddings(Embeddings):
    """Sentence-BERT embeddings wrapper for LangChain."""
    
    def __init__(self, model_name: str = None):
        """Initialize Sentence-BERT model."""
        self.model_name = model_name or settings.embedding_model
        self.model = SentenceTransformer(self.model_name)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents."""
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query."""
        embedding = self.model.encode([text], convert_to_numpy=True)
        return embedding[0].tolist()


class DatabricksVectorSearchRetriever:
    """Databricks Vector Search integration for document retrieval."""
    
    def __init__(self, embeddings: Embeddings):
        """Initialize Databricks Vector Search retriever."""
        self.embeddings = embeddings
        self.endpoint = settings.databricks_vector_search_endpoint
        self.index_name = settings.vector_search_index
        self.top_k = settings.top_k_results
        
    def retrieve(self, query: str, top_k: Optional[int] = None) -> List[Document]:
        """
        Retrieve relevant documents for a query.
        
        Note: This is a simplified implementation. In production, you would
        integrate with the actual Databricks Vector Search SDK.
        """
        k = top_k or self.top_k
        query_embedding = self.embeddings.embed_query(query)
        
        # Placeholder for actual Databricks Vector Search integration
        # In production, use databricks-vectorsearch SDK
        documents = [
            Document(
                page_content=f"Retrieved document {i+1} for query: {query}",
                metadata={"source": f"databricks_vector_search_{i+1}", "score": 0.9 - i*0.1}
            )
            for i in range(k)
        ]
        
        return documents


class AWSBedrockInference:
    """AWS Bedrock inference engine for Claude and Titan models."""
    
    def __init__(self):
        """Initialize AWS Bedrock client."""
        self.bedrock_client = boto3.client(
            'bedrock-runtime',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )
        self.model_id = settings.aws_bedrock_model
    
    def invoke(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """
        Invoke AWS Bedrock model for inference.
        
        Args:
            prompt: The input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated text response
        """
        # Prepare request body based on model type
        if "claude" in self.model_id.lower():
            body = json.dumps({
                "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
                "max_tokens_to_sample": max_tokens,
                "temperature": temperature,
                "top_p": 0.9,
            })
        elif "titan" in self.model_id.lower():
            body = json.dumps({
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": max_tokens,
                    "temperature": temperature,
                    "topP": 0.9,
                }
            })
        else:
            raise ValueError(f"Unsupported model: {self.model_id}")
        
        try:
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=body,
                contentType='application/json',
                accept='application/json'
            )
            
            response_body = json.loads(response['body'].read())
            
            # Extract text based on model type
            if "claude" in self.model_id.lower():
                return response_body.get('completion', '')
            elif "titan" in self.model_id.lower():
                results = response_body.get('results', [])
                return results[0].get('outputText', '') if results else ''
            
        except Exception as e:
            # Return a placeholder response for development/testing
            return f"[Bedrock Response Placeholder] Query processed: {prompt[:100]}..."


class RAGPipeline:
    """Complete RAG pipeline orchestrating embeddings, retrieval, and inference."""
    
    def __init__(self):
        """Initialize RAG pipeline components."""
        self.embeddings = SentenceBERTEmbeddings()
        self.retriever = DatabricksVectorSearchRetriever(self.embeddings)
        self.llm = AWSBedrockInference()
    
    def query(self, question: str, context_length: int = 5) -> Dict[str, Any]:
        """
        Process a RAG query end-to-end.
        
        Args:
            question: User question
            context_length: Number of context documents to retrieve
            
        Returns:
            Dictionary containing answer and metadata
        """
        # Retrieve relevant documents
        documents = self.retriever.retrieve(question, top_k=context_length)
        
        # Build context from retrieved documents
        context = "\n\n".join([doc.page_content for doc in documents])
        
        # Create augmented prompt
        augmented_prompt = f"""Context information:
{context}

Question: {question}

Please provide a detailed answer based on the context above."""
        
        # Generate answer using LLM
        answer = self.llm.invoke(augmented_prompt)
        
        return {
            "question": question,
            "answer": answer,
            "context_documents": [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in documents
            ],
            "num_documents_retrieved": len(documents)
        }
