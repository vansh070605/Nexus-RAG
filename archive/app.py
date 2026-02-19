from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import rag_helper
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global storage for the current document's vector database
# In a real app, you'd use a session or a database
current_vector_db = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global current_vector_db
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Process the PDF into vectors
            current_vector_db = rag_helper.process_pdf(filepath)
            return jsonify({"message": f"Successfully processed {filename}", "filename": filename})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            # Optional: remove file after processing to save space
            if os.path.exists(filepath):
                os.remove(filepath)
                
    return jsonify({"error": "Invalid file type. Only PDFs are supported."}), 400

@app.route('/ask', methods=['POST'])
def ask():
    global current_vector_db
    if current_vector_db is None:
        return jsonify({"error": "Please upload a document first."}), 400
    
    data = request.json
    query = data.get('query')
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    try:
        answer = rag_helper.ask_rag_agent(current_vector_db, query)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(
        debug=True,
        port=5000,
        use_reloader=False  # Prevents watchdog from restarting server on torch/venv file changes
    )
