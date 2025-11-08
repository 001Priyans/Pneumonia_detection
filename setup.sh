#!/bin/bash

# Setup script for Pneumonia Detection Application

echo "========================================"
echo "Pneumonia Detection App Setup"
echo "========================================"

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1)
echo "Found: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo ""
echo "Creating necessary directories..."
mkdir -p uploads
mkdir -p models

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Place your trained model file in the 'models/' directory"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Run the application: python app.py"
echo "4. Open your browser to: http://localhost:5000"
echo ""
echo "========================================"
