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
.
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

## ☁️ Deployment (Render)

1. **New Web Service**: Connect your GitHub repo to [Render](https://render.com).
2. **Environment Variables**:
   - `GROQ_API_KEY`: Your key from Groq Console.
   - `GROQ_MODEL`: `llama-3.1-8b-instant` (optional).
   - `PYTHON_VERSION`: `3.11.0` (recommended).
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `gunicorn run:app`

## 🔺 Deployment (Vercel)

1. **New Project**: Import your GitHub repo into [Vercel](https://vercel.com).
2. **Framework Preset**: Choose **"Other"** (it will auto-detect `vercel.json`).
3. **Environment Variables**:
   - `GROQ_API_KEY`: Your key.
   - `VERCEL`: `1` (required for temp directory switching).
4. **Deploy**: Vercel will build the serverless function and serve your app.

## 🌐 Split Hosting (Recommended for Speed)

If you want the fastest UI response, host the **Frontend** as a static site and the **Backend** on Render.

1.  **Frontend**: Upload the `frontend/` folder to Vercel or Netlify.
2.  **Configuration**: In `frontend/js/app.js`, update `API_BASE_URL` to your Render URL.
3.  **Backend**: Keep the main repository running on Render.

## ⚖️ License
MIT
