from fastapi import FastAPI
from pydantic import BaseModel
from .rag import rag_query

app = FastAPI(title="Enterprise AI Agent Framework")

class QueryPayload(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/rag/query")
def rag_endpoint(payload: QueryPayload):
    result = rag_query(payload.query)
    return result
