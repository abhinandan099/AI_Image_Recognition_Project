import pandas as pd
from datetime import datetime

def log_prediction(image_name, prediction, confidence):

    data = {
        "image_name":[image_name],
        "prediction":[prediction],
        "confidence":[confidence],
        "time":[datetime.now()]
    }

    df = pd.DataFrame(data)

    df.to_csv(
        "logs/predictions.csv",
        mode='a',
        header=False,
        index=False
    )
