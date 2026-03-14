from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def detect_objects(image_path):

    results = model(image_path)

    detected_objects = []

    for r in results:
        for box in r.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            label = model.names[class_id]

            detected_objects.append((label, confidence))

    return detected_objects
