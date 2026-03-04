# Threat Intelligence RAG Assistant

A GenAI retrieval system that processes threat intelligence reports, maps TTPs to MITRE ATT&CK, and generates detection recommendations.

## Features
- Document ingestion (CVE feeds, AWS security bulletins, threat reports)
- Embedding + vector database (FAISS/Chroma)
- Retrieval-Augmented Generation (RAG)
- Grounded ATT&CK mappings
- Evaluation: precision@k and groundedness
- Optional Streamlit or Gradio UI

## Structure
data/
  corpus/

src/
  ingest.py
  embed.py
  rag.py
  evaluate.py

ui/
  app.py

models/
  embeddings/

docker/
  Dockerfile

## Goals
- Automate TI enrichment
- Provide SOC-ready ATT&CK mappings
- Support detection engineering with AI-augmented intelligence
