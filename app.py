"""
Flask Application for Pneumonia Detection
Main application file
"""

import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import sys

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
from model_handler import PneumoniaDetector

# Initialize Flask app
app = Flask(__name__, 
            template_folder='frontend/templates',
            static_folder='frontend/static')

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Model path
MODEL_PATH = 'models/pneumonia_model.h5'

# Initialize model detector
detector = None

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def init_model():
    """Initialize the model detector"""
    global detector
    try:
        if os.path.exists(MODEL_PATH):
            detector = PneumoniaDetector(MODEL_PATH)
            print("Model initialized successfully")
        else:
            print(f"Warning: Model file not found at {MODEL_PATH}")
            print("Please place your trained model file in the 'models' folder")
    except Exception as e:
        print(f"Error initializing model: {str(e)}")

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and prediction"""
    try:
        # Check if model is loaded
        if detector is None:
            return jsonify({
                'success': False,
                'error': 'Model not loaded. Please ensure the model file exists in the models folder.'
            }), 500
        
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            }), 400
        
        file = request.files['file']
        
        # Check if filename is empty
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Check if file is allowed
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Please upload PNG, JPG, or JPEG images.'
            }), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Make prediction
        result = detector.predict(filepath)
        
        # Add filename to result
        result['filename'] = filename
        result['success'] = True
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error processing image: {str(e)}'
        }), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/health')
def health():
    """Health check endpoint"""
    model_loaded = detector is not None
    return jsonify({
        'status': 'running',
        'model_loaded': model_loaded
    }), 200

@app.route('/api/info')
def info():
    """Get application information"""
    return jsonify({
        'name': 'Pneumonia Detection System',
        'version': '1.0.0',
        'description': 'Deep Learning based Pneumonia Detection from Chest X-rays',
        'model': 'VGG19 Transfer Learning',
        'author': 'Your Name'
    }), 200

if __name__ == '__main__':
    # Create upload folder if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize model
    init_model()
    
    # Run app
    print("=" * 60)
    print("Pneumonia Detection System Starting...")
    print("=" * 60)
    print(f"Model Path: {MODEL_PATH}")
    print(f"Upload Folder: {app.config['UPLOAD_FOLDER']}")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
