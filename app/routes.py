# app/routes.py
from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from .k import verify_faces, validate_image

import sys

main = Blueprint('main', __name__)
UPLOAD_FOLDER = 'uploads'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@main.route('/python-version')
def python_version():
    return f"Python version: {sys.version}"
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

    valid_passport, msg_passport = validate_image(passport_path)
    valid_selfie, msg_selfie = validate_image(selfie_path)

    if not valid_passport or not valid_selfie:
        return jsonify({
            'passport_validation': msg_passport,
            'selfie_validation': msg_selfie
        }), 400

    try:
        result = verify_faces(passport_path, selfie_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
