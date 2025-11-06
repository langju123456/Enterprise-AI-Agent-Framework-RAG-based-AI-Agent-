import json
import requests
import streamlit as st

st.set_page_config(page_title="AI Agent RAG (MVP)")

st.title("🔎 Enterprise RAG Demo")
api_url = st.text_input("FastAPI URL", value="http://localhost:8080/rag/query")

query = st.text_input("Enter your question")
if st.button("Ask") and query:
    try:
        resp = requests.post(api_url, json={"query": query}, timeout=30)
        data = resp.json()
        st.subheader("Answer")
        st.write(data.get("answer"))
        st.subheader("Top Contexts")
        st.json(data.get("contexts", []))
    except Exception as e:
        st.error(f"Request failed: {e}")
