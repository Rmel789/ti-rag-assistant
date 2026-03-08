"""
rag.py
Threat Intelligence RAG: Qdrant (local) + SentenceTransformers + OpenAI

Prereqs:
- .env at project root containing: OPENAI_API_KEY=sk-...
- Run: python src/ingest.py
- Run: python src/embed.py  (stores vectors in models/embeddings/qdrant)
"""

from typing import List
from pathlib import Path
import os

# --- Imports you MUST have ---
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from openai import OpenAI

# ---------- Load .env explicitly from project root ----------
PROJECT_ROOT = Path(__file__).resolve().parents[1]  # src/ -> project root
ENV_PATH = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=ENV_PATH)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError(
        f"OPENAI_API_KEY not set. Expected in {ENV_PATH}. "
        "Create .env at the project root."
    )

# ---------- Constants (must match embed.py) ----------
QDRANT_PATH = str(PROJECT_ROOT / "models" / "embeddings" / "qdrant")
COLLECTION = "ti_rag_corpus"
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
OPENAI_MODEL = "gpt-4o-mini"   # change if your account requires a different model

# ---------- Clients (initialized once) ----------
q_client = QdrantClient(path=QDRANT_PATH)               # local file-based Qdrant
embed_model = SentenceTransformer(EMBED_MODEL_NAME)      # for query embeddings
oa = OpenAI(api_key=OPENAI_API_KEY)


def retrieve(query: str, top_k: int = 4) -> List[str]:
    """
    Vector search in Qdrant; returns top_k chunk texts.
    """
    q_vec = embed_model.encode([query])[0].tolist()
    res = q_client.search(
        collection_name=COLLECTION,
        query_vector=q_vec,
        limit=top_k,
        with_payload=True,
    )
    return [hit.payload.get("text", "") for hit in res if hit.payload]


def generate_answer(query: str) -> str:
    """
    RAG flow: retrieve -> build prompt -> call OpenAI -> return answer.
    """
    contexts = retrieve(query, top_k=4)
    context_block = "\n\n---\n".join([c for c in contexts if c.strip()]) or "No context."

    prompt = f"""You are a helpful Threat Intelligence assistant.
Use the CONTEXT to answer the QUESTION. If the answer is not in the context, say "I don't know".

CONTEXT:
{context_block}

QUESTION:
{query}

FINAL ANSWER:
"""

    resp = oa.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return resp.choices[0].message.content


# Optional wrapper for compatibility with an earlier stub name
def run_rag(query: str) -> str:
    return generate_answer(query)


if __name__ == "__main__":
    print(generate_answer("What TTPs are mentioned for FIN7?"))