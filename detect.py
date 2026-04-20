import os
from ultralytics import YOLO

# Load model once
model = YOLO("yolov8n.pt")


def detect_objects(image_path, output_path="output.jpg"):
    if not os.path.exists(image_path):
        return [], None

    try:
        results = model(image_path)

        if not results or len(results) == 0:
            return [], None

        result = results[0]

        if result.boxes is None:
            return [], None

        names = model.names
        detections = []
        image_height, image_width = result.orig_shape
        image_area = float(image_width * image_height) if image_width and image_height else 1.0

        for box in result.boxes:
            cls_id = int(box.cls[0])
            confidence = float(box.conf[0])
            x1, y1, x2, y2 = [float(value) for value in box.xyxy[0].tolist()]
            box_width = max(0.0, x2 - x1)
            box_height = max(0.0, y2 - y1)
            area = box_width * box_height
            area_percent = (area / image_area) * 100

            detections.append(
                {
                    "name": names[cls_id],
                    "confidence": confidence,
                    "confidence_percent": round(confidence * 100, 1),
                    "area_percent": round(area_percent, 1),
                    "bbox": {
                        "x1": round(x1, 1),
                        "y1": round(y1, 1),
                        "x2": round(x2, 1),
                        "y2": round(y2, 1),
                        "width_percent": round((box_width / image_width) * 100, 2),
                        "height_percent": round((box_height / image_height) * 100, 2),
                        "left_percent": round((x1 / image_width) * 100, 2),
                        "top_percent": round((y1 / image_height) * 100, 2),
                    },
                }
            )

        detections.sort(key=lambda item: item["area_percent"], reverse=True)

        # Save result image
        result.save(filename=output_path)

        return detections, output_path

    except Exception as e:
        print("Error:", e)
        return [], None
