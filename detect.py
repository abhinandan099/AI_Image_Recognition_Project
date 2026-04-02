from ultralytics import YOLO
import cv2
import os

model = YOLO("yolov8n.pt")

def detect_objects(image_path):
    if not os.path.exists(image_path):
        raise ValueError("❌ Image path does not exist")

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("❌ Image is empty or corrupted")

    # FIX: pass image instead of path
    results = model(image)

    detected_objects = []

    for r in results:
        for box in r.boxes:
            cls = int(box.cls)
            conf = float(box.conf)
            label = model.names[cls]

            detected_objects.append((label, conf))

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            cv2.rectangle(image, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(
                image,
                f"{label} {conf:.2f}",
                (x1, y1-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,255,0),
                2
            )

    output_path = "output.jpg"
    cv2.imwrite(output_path, image)

    return detected_objects, output_path