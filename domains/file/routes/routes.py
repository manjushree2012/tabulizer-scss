import os
from flask import Blueprint, request, jsonify
from tasks import long_running_task

file_bp = Blueprint('file', __name__)

UPLOAD_DIR = 'uploads'

@file_bp.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(file_path)

    task = long_running_task.delay(file.filename)

    response = {'task_id': task.id, 'status': 'Task started'}
    return jsonify(response), 202