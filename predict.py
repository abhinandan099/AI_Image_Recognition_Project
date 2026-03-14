import cv2
import numpy as np
import tensorflow as tf

# Load trained model
model = tf.keras.models.load_model("model/food_classifier.h5")

def predict_image(image_path):

    img = cv2.imread(image_path)

    img = cv2.resize(img,(150,150))

    img = img/255.0

    img = np.reshape(img,(1,150,150,3))

    prediction = model.predict(img)

    if prediction[0][0] > 0.5:
        label = "Stale"
        confidence = prediction[0][0]
    else:
        label = "Fresh"
        confidence = 1 - prediction[0][0]

    return label, confidence
