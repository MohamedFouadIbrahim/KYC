# from flask import Flask, jsonify, request
from flask import Flask, Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from k import verify_faces

app = Flask(__name__)

# Sample route
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the Flask API!'})

# Example of a GET route
@app.route('/greet/<name>', methods=['GET'])
def greet(name):
    return jsonify({'greeting': f'Hello, {name}!'})

# Example of a POST route
@app.route('/add', methods=['POST'])
def add_numbers():
    data = request.get_json()
    num1 = data.get('num1')
    num2 = data.get('num2')
    if num1 is None or num2 is None:
        return jsonify({'error': 'Missing numbers'}), 400
    return jsonify({'result': num1 + num2})

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

if __name__ == '__main__':
    app.run(debug=True,port=3001)
