import os
from flask import Blueprint, request, jsonify

file_bp = Blueprint('file', __name__)

UPLOAD_DIR = 'uploads'

@file_bp.route('/upload', methods=['POST'])
def create_notes():
    file = request.files['file']
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(file_path)

    response = {'state': 12, 'error': 'asas'}
    return jsonify(response)