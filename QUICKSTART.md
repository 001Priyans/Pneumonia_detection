# Quick Start Guide

## Getting Your Application Running in 5 Minutes

### Step 1: Extract Your Model

From your Jupyter notebook, you already saved your model. Copy it to the models folder:

```bash
# If your model is in the current directory
cp model_weights/vgg19_model_01.h5 pneumonia-detection-app/models/pneumonia_model.h5
```

Or update the filename in `app.py`:
```python
MODEL_PATH = 'models/vgg19_model_01.h5'  # Change this line
```

### Step 2: Install Dependencies

```bash
cd pneumonia-detection-app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
python app.py
```

### Step 4: Open in Browser

Navigate to: `http://localhost:5000`

## Testing Your Application

1. Upload a chest X-ray image
2. Click "Analyze X-ray"
3. View the prediction results

## Common Issues

### Issue: Module not found
**Solution**: Make sure you activated the virtual environment
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Issue: Model file not found
**Solution**: Check the model file is in the `models/` directory and the filename matches in `app.py`

### Issue: Port already in use
**Solution**: Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

## Next Steps

1. **Customize**: Update the README.md with your information
2. **Git**: Initialize git and push to GitHub
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Pneumonia detection app"
   git remote add origin your-repo-url
   git push -u origin main
   ```
3. **Deploy**: Consider deploying to:
   - Heroku
   - AWS
   - Google Cloud
   - Azure
   - DigitalOcean

## For Recruiters

### Project Highlights

✓ **Full-Stack Development**: Backend (Flask/Python) + Frontend (HTML/CSS/JS)
✓ **Deep Learning**: VGG19 transfer learning implementation
✓ **RESTful API**: Clean API design with proper error handling
✓ **Modern UI/UX**: Responsive design with Bootstrap
✓ **Production Ready**: Includes Docker, testing, documentation
✓ **Best Practices**: Modular code, proper project structure

### Technologies Demonstrated

- Python, Flask
- TensorFlow, Keras
- Deep Learning, CNN, Transfer Learning
- RESTful API Design
- HTML5, CSS3, JavaScript
- Bootstrap, Responsive Design
- Docker, Git
- Software Architecture

### Key Features to Highlight

1. Implemented VGG19 transfer learning for medical image classification
2. Built RESTful API with Flask for model inference
3. Created responsive web interface with real-time predictions
4. Designed modular architecture following best practices
5. Included comprehensive documentation and testing
