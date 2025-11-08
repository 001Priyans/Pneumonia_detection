# 🫁 Pneumonia Detection System

An AI-powered web application for detecting pneumonia from chest X-ray images using deep learning. Built with VGG19 transfer learning architecture and Flask.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

- **Deep Learning Model**: VGG19 CNN architecture with transfer learning
- **User-Friendly Interface**: Modern, responsive web interface
- **Real-Time Predictions**: Instant analysis of chest X-ray images
- **Confidence Scores**: Detailed probability breakdown for each prediction
- **Drag & Drop Upload**: Easy file upload with drag-and-drop support
- **RESTful API**: Clean API endpoints for integration

## 🏗️ Project Structure

```
pneumonia-detection-app/
├── app.py                          # Main Flask application
├── backend/
│   └── model_handler.py            # Model loading and prediction logic
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css          # Custom styles
│   │   └── js/
│   │       └── main.js            # Frontend JavaScript
│   └── templates/
│       └── index.html             # Main HTML template
├── models/
│   └── pneumonia_model.h5         # Trained model file (to be added)
├── uploads/                        # Temporary upload directory
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/pneumonia-detection-app.git
   cd pneumonia-detection-app
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Linux/Mac
   source venv/bin/activate
   
   # On Windows
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your trained model**
   - Place your trained model file (`pneumonia_model.h5` or `vgg19_model_01.h5`) in the `models/` directory
   - Update the `MODEL_PATH` in `app.py` if using a different filename

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser and navigate to: `http://localhost:5000`

## 🔧 Usage

### Web Interface

1. Navigate to the application in your web browser
2. Click or drag-and-drop a chest X-ray image (JPG, JPEG, or PNG)
3. Click "Analyze X-ray" button
4. View the prediction results with confidence scores

### API Endpoints

#### Health Check
```http
GET /health
```

Response:
```json
{
  "status": "running",
  "model_loaded": true
}
```

#### Upload and Predict
```http
POST /upload
Content-Type: multipart/form-data
```

Request:
- `file`: Image file (JPG, JPEG, PNG)

Response:
```json
{
  "success": true,
  "prediction": "PNEUMONIA",
  "confidence": 95.67,
  "probabilities": {
    "NORMAL": 4.33,
    "PNEUMONIA": 95.67
  },
  "filename": "xray_image.jpg"
}
```

#### Application Info
```http
GET /api/info
```

## 🧠 Model Architecture

The system uses a **VGG19** convolutional neural network with transfer learning:

- **Base Model**: VGG19 pre-trained on ImageNet
- **Input Size**: 128x128x3 RGB images
- **Custom Layers**:
  - Flatten layer
  - Dense layer (4608 units, ReLU activation)
  - Dropout layer (0.2)
  - Dense layer (1152 units, ReLU activation)
  - Output layer (2 units, Softmax activation)
- **Optimizer**: SGD with learning rate 0.0001
- **Loss Function**: Categorical Crossentropy

### Training Details

- **Dataset**: Chest X-ray Pneumonia Dataset
- **Image Augmentation**: Rotation, flipping, shifting, shearing
- **Callbacks**: Early stopping, model checkpointing, learning rate reduction
- **Validation**: Separate validation and test sets

## 📊 Performance

The model achieves:
- High accuracy on test dataset
- Robust predictions with confidence scores
- Real-time inference capability

*Note: For production use, always validate with medical professionals*

## 🛠️ Technologies Used

- **Backend**: Flask, Python
- **Deep Learning**: TensorFlow, Keras
- **Image Processing**: OpenCV, NumPy
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Bootstrap 5
- **Icons**: Font Awesome

## 📁 Dataset

The model was trained on the [Chest X-Ray Images (Pneumonia) dataset](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia) from Kaggle.

Dataset structure:
- Training images: ~5,000 images
- Validation images: ~16 images
- Test images: ~600 images
- Classes: NORMAL, PNEUMONIA

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment (with Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment
```dockerfile
# Create a Dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🔐 Security Considerations

- File size limited to 16MB
- Only image files (JPG, JPEG, PNG) allowed
- Secure filename handling
- Input validation and error handling

## 📝 Future Enhancements

- [ ] Add user authentication
- [ ] Store prediction history
- [ ] Support for batch predictions
- [ ] Model performance metrics dashboard
- [ ] Multi-language support
- [ ] Mobile application
- [ ] Integration with PACS systems

## ⚠️ Disclaimer

This application is for **educational and research purposes only**. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical decisions.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Name](https://linkedin.com/in/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- VGG19 architecture by Visual Geometry Group, Oxford
- Chest X-Ray dataset by Paul Mooney on Kaggle
- TensorFlow and Keras teams
- Flask framework
- Bootstrap and Font Awesome

## 📸 Screenshots

### Home Page
![Home Page](screenshots/home.png)

### Upload Interface
![Upload](screenshots/upload.png)

### Results Display
![Results](screenshots/results.png)

---

**Made with ❤️ and Deep Learning**
