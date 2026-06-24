import os
import sys

# Add root to python path so it can import backend
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend import create_app

# Vercel Serverless Function entrypoint
app = create_app()
