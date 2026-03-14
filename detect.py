from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

def detect_objects(image_path):

    results = model(image_path)

    detected_objects = []
    image = cv2.imread(image_path)

    for r in results:
        for box in r.boxes:

            cls = int(box.cls)
            conf = float(box.conf)

            label = model.names[cls]

            detected_objects.append((label, conf))

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            cv2.rectangle(image, (x1,y1), (x2,y2), (0,255,0), 2)

            cv2.putText(
                image,
                f"{label} {conf:.2f}",
                (x1, y1-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,255,0),
                2
            )

    cv2.imwrite("output.jpg", image)

    return detected_objects, "output.jpg"
