"""
app/routes.py — Flask Route Handlers
All HTTP endpoints for the Nexus RAG application.
"""
from flask import Blueprint, render_template, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os

from ..core.rag_engine import process_pdf, ask

main = Blueprint("main", __name__)

# In-memory store for the current session's vector DB.
# In a production app this should be per-session (Redis / DB-backed).
_current_vector_db = None


# ── Pages ──────────────────────────────────────────────────────────────────────

@main.route("/")
def index():
    """Serve the main SPA page."""
    return render_template("index.html")


# ── API: Upload PDF ────────────────────────────────────────────────────────────

@main.route("/upload", methods=["POST"])
def upload_file():
    """
    POST /upload
    Accepts a multipart PDF file, processes it into a FAISS vector store,
    and stores it in module-level state for subsequent /ask calls.
    """
    global _current_vector_db

    if "file" not in request.files:
        return jsonify({"error": "No file provided in the request."}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported."}), 415

    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    try:
        _current_vector_db = process_pdf(filepath)
        return jsonify({
            "message": f"'{filename}' processed successfully.",
            "filename": filename,
        })
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
    finally:
        # Clean up the temp file after processing
        if os.path.exists(filepath):
            os.remove(filepath)


# ── API: Ask a Question ────────────────────────────────────────────────────────

@main.route("/ask", methods=["POST"])
def ask_question():
    """
    POST /ask
    Body: { "query": "<user question>" }
    Returns: { "answer": "<LLM answer>" }
    """
    global _current_vector_db

    if _current_vector_db is None:
        return jsonify({"error": "No document indexed yet. Please upload a PDF first."}), 400

    data = request.get_json(silent=True)
    if not data or not data.get("query", "").strip():
        return jsonify({"error": "No query provided."}), 400

    query = data["query"].strip()

    try:
        answer = ask(_current_vector_db, query)
        return jsonify({"answer": answer})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
