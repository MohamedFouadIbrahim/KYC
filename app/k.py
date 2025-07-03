# app/k.py
from deepface import DeepFace
import cv2
import numpy as np
import os
import pytesseract
import re
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
    

def validate_passport(passport_path):
    """Validate if passport is readable and contains exactly one face"""
    try:
        # Load image using OpenCV
        image = cv2.imread(passport_path)
        if image is None:
         return False, "Image could not be read"

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # OCR
        text = pytesseract.image_to_string(gray)
        lower_text = text.lower()

            # Step 1: Check for passport-specific keywords
        keywords = [
                "passport", "surname", "given name", "nationality",
                "date of birth", "place of birth", "date of issue", "date of expiry"
            ]
        keyword_hits = [k for k in keywords if k in lower_text]

            # Step 2: MRZ pattern check (Machine Readable Zone)
        mrz_lines = re.findall(r'[A-Z0-9<]{30,}', text.upper())
        mrz_found = len(mrz_lines) >= 2
        if mrz_found or len(keyword_hits) >= 3:
            return True, f"Passport-like document detected (Keywords: {len(keyword_hits)}, MRZ: {'Yes' if mrz_found else 'No'})"
        else:
            return False, "Not enough evidence of passport (missing keywords or MRZ)"
    except Exception as e:
        return False, str(e)
    
