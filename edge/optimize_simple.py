import tensorflow as tf
import os

print("Starting optimization...")
print("Loading model...")
model = tf.keras.models.load_model('edge/models/health_model.h5')
original_size = os.path.getsize('edge/models/health_model.h5') / (1024*1024)
print(f"Original size: {original_size:.2f} MB")

print("Converting to TFLite...")
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

tflite_path = 'edge/models/health_model.tflite'
with open(tflite_path, 'wb') as f:
    f.write(tflite_model)
tflite_size = os.path.getsize(tflite_path) / (1024*1024)
print(f"TFLite size: {tflite_size:.2f} MB")

import gzip
compressed_path = 'edge/models/health_model.tflite.gz'
with open(tflite_path, 'rb') as f_in:
    with gzip.open(compressed_path, 'wb') as f_out:
        f_out.writelines(f_in)
compressed_size = os.path.getsize(compressed_path) / (1024*1024)
print(f"Compressed size: {compressed_size:.2f} MB")

reduction = ((original_size - compressed_size) / original_size) * 100
print(f"\n✅ DONE!")
print(f"Original: {original_size:.2f} MB")
print(f"Optimized: {compressed_size:.2f} MB")
print(f"Reduction: {reduction:.1f}%")
