# app/k.py
from deepface import DeepFace

def verify_faces(passport_path, selfie_path):
    result = DeepFace.verify(img1_path=passport_path, img2_path=selfie_path)
    return result
