# Pneumonia Detection Model

## Model Not Included

The trained model file (`pneumonia_model.h5` - 405MB) is **not included** in this repository due to GitHub's 100MB file size limit.

## How to Get the Model

### Option 1: Train It Yourself (Recommended)

1. Open the Jupyter notebook: `Pneumonia_Detection_Using_Deep_Learning.ipynb`
2. Download the dataset from [Kaggle](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)
3. Train the model (change `epochs=1` to `epochs=20` for better accuracy)
4. Save the trained model to this directory as `pneumonia_model.h5`

### Option 2: Create a Demo Model

For quick testing and demonstration purposes:

```bash
python create_model.py
```

This creates a model with the correct architecture. Note: It will have random weights for classification layers, so predictions may not be accurate. This is useful for:
- Testing the application
- Demonstrating the UI/UX
- Showing the full-stack implementation

### Option 3: Download Pre-trained Model

If you have access to a pre-trained model:
1. Download the model file
2. Place it in this directory as `pneumonia_model.h5`
3. Restart the Flask application

## Model Architecture

- **Base Model**: VGG19 (pre-trained on ImageNet)
- **Input Size**: 128x128x3 RGB images
- **Custom Layers**:
  - Flatten
  - Dense(4608, activation='relu')
  - Dropout(0.2)
  - Dense(1152, activation='relu')
  - Dense(2, activation='softmax')
- **Classes**: 
  - Index 0: NORMAL
  - Index 1: PNEUMONIA

## Important Notes

⚠️ **For Portfolio/Demo**: The application architecture is production-ready and fully functional. The model needs proper training (15-20 epochs) for accurate predictions in real-world use.

✅ **What This Demonstrates**:
- Full-stack ML application development
- Model integration and deployment
- REST API design
- Modern web interface
- Production-ready code structure

## Model Performance (When Properly Trained)

With 15-20 epochs of training on the full dataset:
- Expected accuracy: 85-95%
- Training time: 2-3 hours (GPU) or 6-8 hours (CPU)
- Dataset: ~5,800 training images, 600 test images
