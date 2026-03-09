# 🛰️ TI‑RAG Assistant  
*A Threat Intelligence Retrieval‑Augmented Generation pipeline*

This project is a complete **Threat Intelligence RAG (Retrieval‑Augmented Generation)** system built with:

- **Python**
- **Streamlit** (UI)
- **SentenceTransformers** (embeddings)
- **Qdrant local vector store**
- **OpenAI API** (LLM backend)
- **Secure .env secrets management**

---

## 🚀 Features

### 🔹 1. Ingestion Pipeline  
Reads `.txt` and `.md` reports from `data/corpus/`, cleans them, and assembles a unified corpus.

### 🔹 2. Embedding & Vector Store  
Chunks the corpus → embeds using `all-MiniLM-L6-v2` → stores vectors in a **local** Qdrant instance (no cloud needed).

### 🔹 3. Retrieval Augmentation  
Semantic search retrieves the most relevant context for a question.

### 🔹 4. LLM Response  
A contextual answer is generated using OpenAI (`gpt‑4o‑mini` or user‑defined).

### 🔹 5. Streamlit UI  
Ask natural‑language questions about your threat intelligence corpus.  
Optional debug tools show:
- retrieved chunks  
- retrieval scores  
- prompt construction  
- and more  

---

## 📂 Project Structure
ti-rag-assistant/
│── src/
│   ├── ingest.py
│   ├── embed.py
│   ├── rag.py
│   └── utils/
│       └── logging_config.py
│── ui/
│   └── app.py
│── data/
│   └── corpus/
│       ├── fin7_sample.md
│       └── placeholder.txt
│── models/
│   └── embeddings/qdrant/  (auto‑generated)
│── requirements.txt
│── README.md
└── .gitignore

---

## 🛠️ Setup

### 1. Create venv  

python -m venv venv
source venv/Scripts/activate

### 2. Install dependencies  

pip install -r requirements.txt

### 3. Add your OpenAI key  
Create a `.env` file in the project root:


OPENAI_API_KEY=sk-...

Do NOT commit this file.

---

## ▶️ Running the Pipeline

### Build corpus:

python src/ingest.py

### Embed & store vectors:

python src/embed.py

### Run the Streamlit UI:

streamlit run ui/app.py

---

## 🧠 Example Questions  
Try inputs like:

- *“What TTPs are mentioned for FIN7?”*  
- *“Summarize the threat actors in the corpus.”*  
- *“List all MITRE ATT&CK techniques referenced.”*

---

## 🛡️ Security  
- Secrets stored in `.env`  
- `.gitignore` protects sensitive data  
- Qdrant runs locally—no external data transfer

---

## 📸 Screenshots (add these)
You can add:
- The UI input box  
- The evidence panel  
- Terminal showing “Stored N chunks in Qdrant”  
- Your VS Code folder tree  

---

## 🌐 Author  
Built by **Renee**, cybersecurity student and aspiring threat intelligence / blue team engineer.

Connect with me on LinkedIn!  
