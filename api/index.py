"""
run.py — Application Entry Point
Run this file to start the Nexus RAG development server.

Usage:
    python run.py
"""
import os
import sys

# Add the root directory to the python path so that 'app' can be found
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000,
        use_reloader=False,  # Disabled: prevents torch/venv file-change restarts
    )
