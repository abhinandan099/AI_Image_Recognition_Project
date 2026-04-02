from ultralytics import YOLO
import cv2
import os

# Load model once
model = YOLO("yolov8n.pt")


def detect_objects(image_path):
    if not os.path.exists(image_path):
        return [], None

    try:
        results = model(image_path)

        if results is None or len(results) == 0:
            return [], None

        result = results[0]

        if result.boxes is None:
            return [], None

        boxes = result.boxes
        names = model.names

        detected_objects = []

        for box in boxes:
            cls_id = int(box.cls[0])
            label = names[cls_id]
            detected_objects.append(label)

        # Save output image
        output_path = "output.jpg"
        result.save(filename=output_path)

        return list(set(detected_objects)), output_path

    except Exception as e:
        print("Error:", e)
        return [], None