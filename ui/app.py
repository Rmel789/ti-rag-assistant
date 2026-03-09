# ui/app.py
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# --- Make sure we can import modules from src/ ---
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))  # put src/ on the import path

# --- Load .env from project root ---
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

st.set_page_config(page_title="TI‑RAG Assistant", page_icon="🛰️", layout="centered")
st.title("🛰️ TI‑RAG Assistant")

# --- Now imports will work because src/ is on sys.path ---
try:
    from rag import generate_answer
    # optional evidence helper if you added it
    try:
        from rag import retrieve_hits
    except Exception:
        retrieve_hits = None
except Exception as e:
    st.error("Failed to import pipeline. See details below:")
    st.exception(e)
    st.stop()

query = st.text_input(
    "Ask a question about your corpus",
    placeholder="e.g., What TTPs are mentioned for FIN7?"
)

if query:
    try:
        with st.spinner("Thinking..."):
            answer = generate_answer(query)
        st.subheader("Answer")
        st.write(answer)

        if retrieve_hits:
            with st.expander("Show evidence (top matches)"):
                hits = retrieve_hits(query, top_k=4)
                for i, (text, score) in enumerate(hits, start=1):
                    st.markdown(f"**Result {i}** — score: `{score}`")
                    st.code((text[:1200] + '…') if len(text) > 1200 else text, language="markdown")
    except Exception as e:
        st.error("An error occurred while generating the answer:")
        st.exception(e)
