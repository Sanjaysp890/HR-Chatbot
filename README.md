# RAG HR Chatbot - Starter

## What this repo contains
- Ingest script to parse PDFs and build FAISS index.
- FastAPI backend (`api.py`) exposing `/query`.
- Streamlit UI (`ui_streamlit.py`) to chat.
- Dockerfile to containerize backend.

## Quick start (local)
1. Put `HR-Policy (1).pdf` into `data/` folder.
2. Install deps: `pip install -r requirements.txt`
3. Build index: `python ingest.py`
4. Run backend: `uvicorn api:app --reload --port 8000`
5. Run UI in separate terminal: `streamlit run ui_streamlit.py`

## Notes
- Set `OPENAI_API_KEY` as env var before running backend.
- This is starter code; re-ranking and caching are minimal placeholders.
