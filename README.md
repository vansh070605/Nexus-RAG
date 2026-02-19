# 🧠 Nexus RAG — Artificial Intelligence Augmented

Nexus RAG is a minimalist, high-performance Retrieval Augmented Generation (RAG) platform. It allows you to upload PDF documents and interrogate them using semantic search and cutting-edge LLMs.

## 🚀 Quick Start

1. **Setup Environment**:
   - Clone the repository.
   - Create a virtual environment: `python -m venv .venv`
   - Activate it: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Mac/Linux)
   - Install dependencies: `pip install -r requirements.txt`

2. **Configure API**:
   - Create a `.env` file based on `.env.example`.
   - Add your `GROQ_API_KEY`.

3. **Run Application**:
   ```bash
   python run.py
   ```
   Open `http://localhost:5000` in your browser.

## 📁 Project Structure

```text
e:/CODING/Lang Chain LLM App/
├── app/                    # Main application package
│   ├── api/                # API blueprints and routes
│   │   └── routes.py
│   ├── core/               # Core business logic (RAG pipeline)
│   │   └── rag_engine.py
│   ├── static/             # Frontend assets (CSS, JS)
│   ├── templates/          # HTML templates
│   └── __init__.py         # App factory
├── uploads/                # Temporary directory for processed PDFs
├── run.py                  # Entry point
├── .env                    # Configuration
└── requirements.txt        # Dependencies
```

## 🛠️ Tech Stack

- **Backend**: Flask, LangChain, FAISS
- **Embeddings**: Sentence-Transformers (`all-MiniLM-L6-v2`)
- **LLM**: Llama 3 (via Groq)
- **Frontend**: Vanilla JS, CSS (Quantum Dark Theme)

## ⚖️ License
MIT
# Nexus-RAG
