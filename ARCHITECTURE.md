# Application Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                          │
│                    (Web Browser)                             │
│  - Upload chest X-ray                                        │
│  - View predictions                                          │
│  - See confidence scores                                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ HTTP Request
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    FLASK APPLICATION                         │
│                       (app.py)                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Routes:                                             │   │
│  │  - GET  /              → Home page                  │   │
│  │  - POST /upload        → Image upload & prediction  │   │
│  │  - GET  /health        → Health check               │   │
│  │  - GET  /api/info      → App information            │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ Calls
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  MODEL HANDLER                               │
│               (backend/model_handler.py)                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  PneumoniaDetector Class:                           │   │
│  │  - load_model()         → Load VGG19 model         │   │
│  │  - preprocess_image()   → Resize & normalize       │   │
│  │  - predict()            → Get prediction           │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ Uses
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    TRAINED MODEL                             │
│              (models/pneumonia_model.h5)                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  VGG19 Architecture:                                │   │
│  │  - Pre-trained VGG19 base                          │   │
│  │  - Custom dense layers                             │   │
│  │  - Softmax output (2 classes)                      │   │
│  │  - Input: 128x128x3 RGB images                     │   │
│  │  - Output: [NORMAL, PNEUMONIA] probabilities       │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

```
1. User uploads X-ray image
         ↓
2. Frontend (main.js) sends file to /upload endpoint
         ↓
3. Flask app (app.py) receives file
         ↓
4. File is saved to uploads/ directory
         ↓
5. model_handler.py preprocesses image:
   - Read image file
   - Convert to RGB
   - Resize to 128x128
   - Normalize (divide by 255)
   - Add batch dimension
         ↓
6. Processed image fed to VGG19 model
         ↓
7. Model outputs probabilities:
   [NORMAL: 0.15, PNEUMONIA: 0.85]
         ↓
8. Results formatted as JSON:
   {
     "prediction": "PNEUMONIA",
     "confidence": 85.0,
     "probabilities": {
       "NORMAL": 15.0,
       "PNEUMONIA": 85.0
     }
   }
         ↓
9. JSON sent back to frontend
         ↓
10. Results displayed with:
    - Prediction label
    - Confidence badge
    - Probability bars
    - Visual styling
```

## Directory Responsibilities

```
pneumonia-detection-app/
│
├── app.py                      # ENTRY POINT
│   - Initialize Flask app
│   - Define routes
│   - Handle HTTP requests/responses
│   - Error handling
│
├── backend/
│   └── model_handler.py        # MODEL INTERFACE
│       - Load and manage model
│       - Image preprocessing
│       - Prediction logic
│
├── frontend/
│   ├── templates/
│   │   └── index.html          # USER INTERFACE
│   │       - Page structure
│   │       - Upload interface
│   │       - Results display
│   │
│   └── static/
│       ├── css/style.css       # STYLING
│       │   - Visual design
│       │   - Responsive layout
│       │   - Animations
│       │
│       └── js/main.js          # INTERACTIVITY
│           - File upload handling
│           - API communication
│           - Dynamic UI updates
│
├── models/
│   └── pneumonia_model.h5      # AI MODEL
│       - Trained VGG19 model
│       - Learned weights
│
└── uploads/                     # TEMPORARY STORAGE
    - User uploaded images
    - Cleaned periodically
```

## Component Interactions

```
┌──────────────┐     sends file      ┌──────────────┐
│   Browser    │ ──────────────────→ │     Flask    │
│  (main.js)   │                     │   (app.py)   │
└──────────────┘                     └──────┬───────┘
       ↑                                    │
       │                                    │ calls
       │ returns JSON                       ▼
       │                          ┌──────────────────┐
       └──────────────────────────│  Model Handler   │
                                  │(model_handler.py)│
                                  └────────┬─────────┘
                                           │
                                           │ uses
                                           ▼
                                  ┌──────────────────┐
                                  │   VGG19 Model    │
                                  │ (.h5 file)       │
                                  └──────────────────┘
```

## Technology Stack

```
┌─────────────────────────────────────────────┐
│              PRESENTATION LAYER              │
│  - HTML5 (Structure)                        │
│  - CSS3 + Bootstrap (Styling)               │
│  - JavaScript (Interactivity)               │
│  - Font Awesome (Icons)                     │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│              APPLICATION LAYER               │
│  - Flask 3.0 (Web Framework)                │
│  - Werkzeug (WSGI Utility)                  │
│  - Gunicorn (WSGI Server)                   │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│              MODEL LAYER                     │
│  - TensorFlow 2.15 (Deep Learning)          │
│  - Keras (High-level API)                   │
│  - VGG19 (CNN Architecture)                 │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│              DATA LAYER                      │
│  - NumPy (Numerical Operations)             │
│  - OpenCV (Image Processing)                │
│  - Pillow (Image Handling)                  │
└─────────────────────────────────────────────┘
```

## API Endpoints

```
GET /
├── Returns: HTML page
└── Purpose: Serve main application interface

POST /upload
├── Accepts: multipart/form-data (image file)
├── Returns: JSON with prediction results
└── Purpose: Process X-ray and return diagnosis

GET /health
├── Returns: JSON with status
└── Purpose: Check server and model status

GET /api/info
├── Returns: JSON with app information
└── Purpose: Provide app metadata
```

## Security Layers

```
┌──────────────────────────────────────┐
│  1. File Type Validation             │
│     - Only JPG, JPEG, PNG allowed    │
└────────────┬─────────────────────────┘
             ▼
┌──────────────────────────────────────┐
│  2. File Size Limit                  │
│     - Maximum 16MB                   │
└────────────┬─────────────────────────┘
             ▼
┌──────────────────────────────────────┐
│  3. Secure Filename                  │
│     - Sanitize user input            │
└────────────┬─────────────────────────┘
             ▼
┌──────────────────────────────────────┐
│  4. Error Handling                   │
│     - Try-catch blocks               │
│     - User-friendly messages         │
└──────────────────────────────────────┘
```

## Deployment Architecture

```
Development:
┌──────────────────────────────────────┐
│  Local Machine                       │
│  - Python 3.8+                       │
│  - Virtual environment               │
│  - Flask dev server                  │
│  - Debug mode ON                     │
└──────────────────────────────────────┘

Production:
┌──────────────────────────────────────┐
│  Cloud Platform (AWS/GCP/Azure)      │
│  ┌────────────────────────────────┐ │
│  │  Docker Container              │ │
│  │  - Gunicorn (4 workers)        │ │
│  │  - Application code            │ │
│  │  - Model files                 │ │
│  └────────────────────────────────┘ │
│  ┌────────────────────────────────┐ │
│  │  Load Balancer                 │ │
│  └────────────────────────────────┘ │
│  ┌────────────────────────────────┐ │
│  │  Persistent Storage            │ │
│  │  - Model files                 │ │
│  └────────────────────────────────┘ │
└──────────────────────────────────────┘
```

---

This architecture provides:
- ✅ Separation of concerns
- ✅ Modularity
- ✅ Scalability
- ✅ Maintainability
- ✅ Testability
