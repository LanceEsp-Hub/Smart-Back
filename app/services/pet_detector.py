import io
from fastapi import UploadFile, HTTPException
from PIL import Image
import torch
import numpy as np
import os

# Load the YOLOv5 model from local file
try:
    # Make sure to use the correct relative path based on where this script runs
    model_path = os.path.join(os.path.dirname(__file__), '../../yolov5s.pt')
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, source='local')
except Exception as e:
    raise RuntimeError(f"Failed to load YOLOv5 model from local file: {str(e)}")

async def verify_pet_image(file: UploadFile):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        if image.mode != 'RGB':
            image = image.convert('RGB')

        results = model(image)
        detections = results.pandas().xyxy[0]

        has_cat = any((detections['class'] == 15) & (detections['confidence'] > 0.3))
        has_dog = any((detections['class'] == 16) & (detections['confidence'] > 0.3))

        detected_objects = detections['name'].unique().tolist() if not detections.empty else []
        max_confidence = float(detections['confidence'].max()) if not detections.empty else 0.0

        return {
            'is_valid': has_cat or has_dog,
            'is_cat': has_cat,
            'is_dog': has_dog,
            'confidence': max_confidence,
            'detected_objects': detected_objects
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": f"Image processing failed: {str(e)}",
                "type": "processing_error"
            }
        )
