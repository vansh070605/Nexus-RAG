import os
import sys

# Add root to python path so it can import backend
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from flask_cors import CORS
from backend.api.routes import main

# Vercel's zero-config AST parser STRICTLY requires `app = Flask(__name__)` literally
app = Flask(__name__)

# Apply the same logic from create_app()
CORS(app)

if os.environ.get("VERCEL"):
    uploads_dir = "/tmp/uploads"
else:
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    uploads_dir = os.path.join(project_root, "uploads")
    
os.makedirs(uploads_dir, exist_ok=True)
app.config["UPLOAD_FOLDER"] = uploads_dir
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

app.register_blueprint(main)
