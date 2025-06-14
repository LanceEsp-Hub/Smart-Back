import io
import os
from fastapi import UploadFile, HTTPException
from PIL import Image
from ultralytics import YOLO
import numpy as np

# Load YOLOv5s model from local file
try:
    model_path = os.path.join(os.path.dirname(__file__), '../../yolov5s.pt')
    model = YOLO(model_path)
except Exception as e:
    raise RuntimeError(f"Failed to load YOLOv5 model from file: {str(e)}")

async def verify_pet_image(file: UploadFile):
    try:
        # Read and open the image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # Ensure RGB format
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Run detection
        results = model(image, verbose=False)[0]

        # Extract detections
        names = model.names  # class index to name
        boxes = results.boxes

        labels = [names[int(cls)] for cls in boxes.cls.tolist()]
        confidences = boxes.conf.tolist()

        # Detect cat/dog presence
        has_cat = any(label == 'cat' and conf > 0.3 for label, conf in zip(labels, confidences))
        has_dog = any(label == 'dog' and conf > 0.3 for label, conf in zip(labels, confidences))

        return {
            'is_valid': has_cat or has_dog,
            'is_cat': has_cat,
            'is_dog': has_dog,
            'confidence': max(confidences) if confidences else 0.0,
            'detected_objects': list(set(labels))
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": f"Image processing failed: {str(e)}",
                "type": "processing_error"
            }
        )
