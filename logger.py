import pandas as pd
from datetime import datetime
import os

def log_prediction(image_name, prediction, confidence):
    os.makedirs("logs", exist_ok=True)

    file_path = "logs/predictions.csv"

    data = {
        "image_name": [image_name],
        "prediction": [prediction],
        "confidence": [confidence],
        "time": [datetime.now()]
    }

    df = pd.DataFrame(data)

    if not os.path.exists(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)