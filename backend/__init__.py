"""
app/__init__.py — Flask Application Factory
"""
from flask import Flask
from flask_cors import CORS
import os


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Allow cross-origin requests (useful if frontend is served separately)
    CORS(app)

    # Ensure uploads directory exists
    # For Vercel/Serverless environments, we must use /tmp
    if os.environ.get("VERCEL"):
        uploads_dir = "/tmp/uploads"
    else:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        uploads_dir = os.path.join(project_root, "uploads")
        
    os.makedirs(uploads_dir, exist_ok=True)
    app.config["UPLOAD_FOLDER"] = uploads_dir
    app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 MB limit

    # Register routes blueprint
    from .api.routes import main
    app.register_blueprint(main)

    return app
