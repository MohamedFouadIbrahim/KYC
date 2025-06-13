# app/routes.py
from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from .k import verify_faces

main = Blueprint('main', __name__)
UPLOAD_FOLDER = 'uploads'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@main.route('/verify', methods=['POST'])
def verify():
    passport = request.files.get('passport')
    selfie = request.files.get('selfie')

    if not passport or not selfie:
        return jsonify({'error': 'Both passport and selfie images are required'}), 400

    passport_path = os.path.join(UPLOAD_FOLDER, secure_filename(passport.filename))
    selfie_path = os.path.join(UPLOAD_FOLDER, secure_filename(selfie.filename))

    passport.save(passport_path)
    selfie.save(selfie_path)

    try:
        result = verify_faces(passport_path, selfie_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
