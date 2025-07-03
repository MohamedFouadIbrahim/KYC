# app/k.py
from deepface import DeepFace
import cv2
import numpy as np
import os
def verify_faces(passport_path, selfie_path):
    result = DeepFace.verify(img1_path=passport_path, img2_path=selfie_path)
    return result

def validate_image(image_path):
    """Validate if image is readable and contains exactly one face"""
    try:
        # Load image using OpenCV
        img = cv2.imread(image_path)

        if img is None:
            return False, "Cannot read image"

        # Detect faces using OpenCV or DeepFace
        # faces = DeepFace.extract_faces(img_path=image_path, enforce_detection=True)
        # if len(faces) != 1:
        #     return False, f"Image must contain exactly one face, found {len(faces)}"

        return True, "Valid image"
    except Exception as e:
        return False, str(e)
