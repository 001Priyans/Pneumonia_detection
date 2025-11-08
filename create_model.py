"""
Script to create the model architecture and save it
Since the notebook was trained for only 1 epoch, this creates the model structure
You can later retrain with more epochs for better accuracy
"""

print("Creating VGG19 model architecture...")
print("Note: This will create a model with random weights.")
print("For production use, you should train it properly with more epochs.\n")

try:
    import tensorflow as tf
    from tensorflow.keras.applications.vgg19 import VGG19
    from tensorflow.keras.models import Model
    from tensorflow.keras.layers import Input, Dense, Flatten, Dropout
    from tensorflow.keras.optimizers import SGD
    import os
    
    print("Building model architecture...")
    
    # Create VGG19 base model
    base_model = VGG19(input_shape=(128, 128, 3),
                       include_top=False,
                       weights='imagenet')
    
    # Freeze base model layers
    for layer in base_model.layers:
        layer.trainable = False
    
    # Add custom layers
    x = base_model.output
    flat = Flatten()(x)
    class_1 = Dense(4608, activation='relu')(flat)
    dropout = Dropout(0.2)(class_1)
    class_2 = Dense(1152, activation='relu')(dropout)
    output = Dense(2, activation='softmax')(class_2)
    
    # Create model
    model = Model(base_model.inputs, output)
    
    # Compile model
    sgd = SGD(learning_rate=0.0001, decay=1e-6, momentum=0.1, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
    
    print("\n✓ Model architecture created successfully!")
    print(f"  Total parameters: {model.count_params():,}")
    
    # Create models directory
    os.makedirs('models', exist_ok=True)
    
    # Save model
    model_path = 'models/pneumonia_model.h5'
    model.save(model_path)
    
    print(f"\n✓ Model saved to: {model_path}")
    print(f"  File size: {os.path.getsize(model_path) / (1024*1024):.2f} MB")
    
    print("\n" + "="*60)
    print("IMPORTANT NOTES:")
    print("="*60)
    print("✓ Model architecture created and saved")
    print("⚠ This model uses pre-trained VGG19 weights (ImageNet)")
    print("⚠ The classification layers have random weights")
    print("\nFor better accuracy, you should:")
    print("1. Go back to your notebook")
    print("2. Train for more epochs (e.g., 10-20 epochs)")
    print("3. Copy the trained model here")
    print("\nFor now, you can use this to TEST the application!")
    print("="*60)
    
    print("\nNext step: Run the application")
    print("  python app.py")
    
except ImportError as e:
    print(f"\n✗ Error: {e}")
    print("\nPlease install TensorFlow first:")
    print("  pip install tensorflow==2.15.0")
    
except Exception as e:
    print(f"\n✗ Error creating model: {e}")
    import traceback
    traceback.print_exc()
