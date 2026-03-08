from pathlib import Path
from typing import List
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels


# ---------- Paths & Constants ----------
DATA_DIR = Path("data/corpus")
CORPUS_FILE = DATA_DIR / "combined_corpus.txt"

QDRANT_PATH = Path("models/embeddings/qdrant")  # local, file-based store
COLLECTION = "ti_rag_corpus"

# Chunking defaults (tune later as needed)
CHUNK_SIZE = 450   # ~words per chunk
OVERLAP = 50       # ~word overlap


# ---------- Helpers ----------
def read_corpus() -> str:
    if not CORPUS_FILE.exists():
        raise FileNotFoundError(
            f"{CORPUS_FILE} not found. Run `python src/ingest.py` first."
        )
    return CORPUS_FILE.read_text(encoding="utf-8")


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> List[str]:
    """Simple word-based chunking with overlap to preserve context."""
    words = text.split()
    chunks: List[str] = []
    i = 0
    step = max(1, chunk_size - overlap)
    while i < len(words):
        chunk = " ".join(words[i : i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
        i += step
    return chunks


def ensure_collection(client: QdrantClient, vector_size: int) -> None:
    """Create/recreate a collection with cosine distance if missing."""
    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION not in collections:
        client.recreate_collection(
            collection_name=COLLECTION,
            vectors_config=qmodels.VectorParams(
                size=vector_size,
                distance=qmodels.Distance.COSINE,
            ),
        )


def main():
    # 1) Load + chunk
    text = read_corpus()
    chunks = chunk_text(text)
    if not chunks:
        print("[WARN] No chunks produced. Is the corpus empty?")
        return

    # 2) Embed with a small, fast model (CPU friendly)
    model = SentenceTransformer("all-MiniLM-L6-v2")  # 384-dim vectors
    embeddings = model.encode(chunks, batch_size=64, show_progress_bar=True)

    # 3) Init local Qdrant (no Docker; persists to disk)
    QDRANT_PATH.mkdir(parents=True, exist_ok=True)
    client = QdrantClient(path=str(QDRANT_PATH))

    # 4) Ensure collection exists with correct vector size
    vector_size = embeddings.shape[1]
    ensure_collection(client, vector_size=vector_size)

    # 5) Upsert points (vector + payload)
    points = [
        qmodels.PointStruct(
            id=idx,
            vector=emb.tolist(),
            payload={"text": txt, "chunk_id": idx},
        )
        for idx, (emb, txt) in enumerate(zip(embeddings, chunks))
    ]
    client.upsert(collection_name=COLLECTION, points=points)

    print(f"[OK] Stored {len(points)} chunks in Qdrant at {QDRANT_PATH}")


if __name__ == "__main__":
    main()
