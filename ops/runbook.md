# Runbook (MVP)
## Local Dev
- `uvicorn app.api.main:app --reload --port 8080`
- `streamlit run app/web/app.py`

## Common Issues
- 401/403 to Bedrock/Databricks: check tokens/region/IAM
- Vector Search empty: confirm index built & permissions
