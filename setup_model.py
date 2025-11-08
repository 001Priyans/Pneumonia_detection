"""
Helper script to copy your trained model to the application
"""

import os
import shutil
from pathlib import Path

def find_model_files():
    """Find potential model files in common locations"""
    search_paths = [
        ".",
        "..",
        "./model_weights",
        "../model_weights",
        "./models",
        "../models"
    ]
    
    model_files = []
    
    for path in search_paths:
        if os.path.exists(path):
            for file in Path(path).rglob("*.h5"):
                model_files.append(str(file))
            for file in Path(path).rglob("*.keras"):
                model_files.append(str(file))
    
    return model_files

def copy_model(source, destination):
    """Copy model file to destination"""
    try:
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.copy2(source, destination)
        return True
    except Exception as e:
        print(f"Error copying file: {e}")
        return False

def main():
    print("=" * 60)
    print("Model File Setup Helper")
    print("=" * 60)
    print()
    
    # Find model files
    print("Searching for model files...")
    model_files = find_model_files()
    
    if not model_files:
        print("No model files found!")
        print()
        print("Please ensure your model file (.h5 or .keras) is in:")
        print("  - Current directory")
        print("  - model_weights/ directory")
        print("  - models/ directory")
        print()
        return
    
    print(f"Found {len(model_files)} model file(s):")
    for i, file in enumerate(model_files, 1):
        size = os.path.getsize(file) / (1024 * 1024)  # Size in MB
        print(f"  {i}. {file} ({size:.2f} MB)")
    
    print()
    
    if len(model_files) == 1:
        choice = 1
        print(f"Using the only model file found: {model_files[0]}")
    else:
        try:
            choice = int(input("Select model file number to use: "))
            if choice < 1 or choice > len(model_files):
                print("Invalid choice!")
                return
        except ValueError:
            print("Invalid input!")
            return
    
    source_file = model_files[choice - 1]
    destination_file = "models/pneumonia_model.h5"
    
    print()
    print(f"Copying: {source_file}")
    print(f"To: {destination_file}")
    
    if copy_model(source_file, destination_file):
        print()
        print("✓ Model file copied successfully!")
        print()
        print("Next steps:")
        print("  1. Run: python app.py")
        print("  2. Open: http://localhost:5000")
    else:
        print()
        print("✗ Failed to copy model file")
        print()
        print("Manual copy command:")
        print(f"  cp {source_file} {destination_file}")

if __name__ == "__main__":
    main()
