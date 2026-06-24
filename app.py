"""
run.py — Application Entry Point
Run this file to start the Nexus RAG development server.

Usage:
    python run.py
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000,
        use_reloader=False,  # Disabled: prevents torch/venv file-change restarts
    )
