"""
Download a pre-trained model to optimize
"""

import tensorflow as tf
import os

print("Downloading model...")

# Download MobileNetV2 (real model, used in industry)
model = tf.keras.applications.MobileNetV2(weights='imagenet')

# Create folder
os.makedirs('edge/models', exist_ok=True)

# Save model
model.save('edge/models/health_model.h5')

# Check size
size = os.path.getsize('edge/models/health_model.h5') / (1024*1024)
print(f"✅ Model saved!")
print(f"✅ Size: {size:.1f} MB")
print(f"✅ Location: edge/models/health_model.h5")