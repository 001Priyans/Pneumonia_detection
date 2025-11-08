"""
Model Handler for Pneumonia Detection
Handles model loading and predictions
"""

import os
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tensorflow as tf

class PneumoniaDetector:
    def __init__(self, model_path):
        """
        Initialize the Pneumonia Detector with a trained model
        
        Args:
            model_path (str): Path to the trained model file
        """
        self.model_path = model_path
        self.model = None
        self.img_size = 128
        # IMPORTANT: flow_from_directory sorts folders alphabetically
        # Folders: NORMAL, PNEUMONIA -> Index 0=NORMAL, 1=PNEUMONIA
        self.class_names = {0: 'NORMAL', 1: 'PNEUMONIA'}
        self.load_model()
    
    def load_model(self):
        """Load the trained model"""
        try:
            if os.path.exists(self.model_path):
                self.model = load_model(self.model_path)
                print(f"Model loaded successfully from {self.model_path}")
            else:
                print(f"Model file not found at {self.model_path}")
                raise FileNotFoundError(f"Model file not found at {self.model_path}")
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise
    
    def preprocess_image(self, img_path):
        """
        Preprocess the image for prediction
        
        Args:
            img_path (str): Path to the image file
            
        Returns:
            numpy.ndarray: Preprocessed image array
        """
        try:
            # Read image
            img = cv2.imread(img_path)
            if img is None:
                raise ValueError("Unable to read image")
            
            # Convert to RGB (OpenCV reads as BGR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Resize to model input size
            img = cv2.resize(img, (self.img_size, self.img_size))
            
            # Normalize pixel values
            img = img / 255.0
            
            # Add batch dimension
            img = np.expand_dims(img, axis=0)
            
            return img
        except Exception as e:
            print(f"Error preprocessing image: {str(e)}")
            raise
    
    def predict(self, img_path):
        """
        Make prediction on an image
        
        Args:
            img_path (str): Path to the image file
            
        Returns:
            dict: Prediction results containing class and confidence
        """
        try:
            # Preprocess image
            processed_img = self.preprocess_image(img_path)
            
            # Make prediction
            predictions = self.model.predict(processed_img, verbose=0)
            
            # Debug: Print raw predictions
            print(f"Raw predictions: {predictions[0]}")
            
            # Get predicted class and confidence
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx]) * 100
            
            # Map to class name
            predicted_class = self.class_names[predicted_class_idx]
            
            print(f"Predicted class: {predicted_class} (index: {predicted_class_idx}, confidence: {confidence:.2f}%)")
            
            result = {
                'prediction': predicted_class,
                'confidence': round(confidence, 2),
                'probabilities': {
                    'NORMAL': round(float(predictions[0][0]) * 100, 2),
                    'PNEUMONIA': round(float(predictions[0][1]) * 100, 2)
                }
            }
            
            return result
        except Exception as e:
            print(f"Error making prediction: {str(e)}")
            raise
    
    def batch_predict(self, img_paths):
        """
        Make predictions on multiple images
        
        Args:
            img_paths (list): List of image file paths
            
        Returns:
            list: List of prediction results
        """
        results = []
        for img_path in img_paths:
            try:
                result = self.predict(img_path)
                results.append(result)
            except Exception as e:
                results.append({'error': str(e)})
        return results
