import tensorflow as tf
import numpy as np
from PIL import Image
import os

MODEL_PATH = "model/food_classifier.keras"

if not os.path.exists(MODEL_PATH):
    raise Exception("❌ Train model first using train_model.py")

model = tf.keras.models.load_model(MODEL_PATH)

def predict_image(image_path):
    try:
        img = Image.open(image_path).convert("RGB")
        img = img.resize((150,150))

        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        pred = model.predict(img_array)[0][0]

        if pred < 0.5:
            return "Fresh", float(1 - pred)
        else:
            return "Stale", float(pred)

    except Exception as e:
        return f"Error: {e}", 0.0