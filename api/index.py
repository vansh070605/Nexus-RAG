from flask import Flask

app = Flask(__name__)

def setup():
    import os
    import sys
    
    # Add the root directory to the python path so that 'app' can be found
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    
    from flask_cors import CORS
    CORS(app)
    
    if os.environ.get("VERCEL") or os.environ.get("VERCEL_URL"):
        uploads_dir = "/tmp/uploads"
    else:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        uploads_dir = os.path.join(project_root, "uploads")
        
    os.makedirs(uploads_dir, exist_ok=True)
    app.config["UPLOAD_FOLDER"] = uploads_dir
    app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024
    
    from app.api.routes import main
    app.register_blueprint(main)

setup()
