# api.py
import os
import re
import logging
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# local import (your retriever implementation)
from retriever import Retriever

# optional groq client import (keep as-is if you have the package)
try:
    from groq import Groq
except Exception:
    Groq = None

# Load env
load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rag-backend")

app = FastAPI(title="RAG HR Chatbot API")

# init retriever (may load vectorstore; keep as you had it)
retr = Retriever()

# Load keys and model from environment but do NOT crash startup if missing
GROQ_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

client = None
if GROQ_KEY and Groq is not None:
    try:
        client = Groq(api_key=GROQ_KEY)
        logger.info("Groq client initialized")
    except Exception as e:
        logger.exception("Failed to initialize Groq client: %s", e)
        client = None
else:
    if not GROQ_KEY:
        logger.warning("GROQ_API_KEY not set; /query will return an error until set.")
    if Groq is None:
        logger.warning("groq package not importable; /query will not call the LLM.")

# Simple in-memory cache
cache = {}

class Query(BaseModel):
    question: str

@app.get("/")
async def root():
    """
    Simple root endpoint to avoid 404 on GET / (useful for healthchecks or quick testing).
    """
    return {"service": "RAG HR Chatbot API", "status": "running", "endpoints": ["/health", "/query"]}

@app.get("/health")
async def health():
    """
    Lightweight health endpoint suitable for Docker healthchecks.
    Keep this extremely cheap and fast.
    """
    return {"status": "ok"}

@app.post("/query")
def query(q: Query):
    """
    Main query endpoint. Returns JSON:
    {
      "answer": "<text or null>",
      "sources": ["file1.pdf", ...],
      "error": "<error message if any>"
    }
    """
    question = q.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="question field must be non-empty")

    # cache lookup
    if question in cache:
        return cache[question]

    # Ensure LLM client available
    if client is None:
        return {
            "answer": None,
            "sources": [],
            "error": "LLM client not configured (GROQ_API_KEY missing or groq package not available)."
        }

    # Retrieve docs (assumes retr.retrieve returns list of dicts with 'text' and 'source')
    try:
        docs = retr.retrieve(question, top_k=5)  # keep your original behavior
    except Exception as e:
        logger.exception("Retriever error: %s", e)
        return {"answer": None, "sources": [], "error": f"Retriever error: {str(e)}"}

    context = "\n\n".join([d.get('text', '') for d in docs])

    prompt = (
        "You are an HR assistant. Use ONLY the context below to answer. "
        "If not present, say 'Not available in HR Policy'.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\n\n"
        "Answer concisely. Do NOT include source names or filenames in the answer text; "
        "return only the answer. (We will provide sources separately.)"
    )

    try:
        # Example Groq call (kept as in your original code)
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=300,
        )
    except Exception as e:
        logger.exception("Groq API call failed: %s", e)
        return {"answer": None, "sources": [], "error": f"Groq API error: {str(e)}"}

    # Extract raw answer safely from possible response shapes
    raw_answer = ""
    try:
        raw_answer = response.choices[0].message.content
    except Exception:
        try:
            raw_answer = response["choices"][0]["message"]["content"]
        except Exception:
            raw_answer = str(response)

    # Remove any inline "(Source: ...)" the model may have added
    answer = re.sub(r'\(\s*Source:.*?\)', '', raw_answer, flags=re.IGNORECASE).strip()
    # normalize whitespace and trim punctuation at ends
    answer = re.sub(r'\s{2,}', ' ', answer).strip()
    answer = re.sub(r'^[\W_]+|[\W_]+$', '', answer).strip()

    sources = list({d.get('source') for d in docs if d.get('source')})

    result = {"answer": answer or None, "sources": sources, "error": None}
    cache[question] = result
    return result
