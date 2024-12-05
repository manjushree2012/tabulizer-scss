import os
from flask import Blueprint, request, jsonify
from tasks import parse_pdf
from setup import celery

file_bp = Blueprint('file', __name__)

UPLOAD_DIR = '/app/uploads'

@file_bp.route('/upload', methods=['POST'])
def upload_file():
    files =  request.files.getlist("file")
    task_ids = {}

    for file in files:
        task = parse_pdf.delay(file.filename)
        task_ids[file.filename] = task.id

        task_dir = os.path.join(UPLOAD_DIR, str(task.id))
        os.makedirs(task_dir, exist_ok=True)

        file_path = os.path.join(task_dir, file.filename)
        file.save(file_path)
    response = {'task_ids': task_ids, 'status': 'Queue started'}
    return jsonify(response), 202

@file_bp.route('/status/<task_id>', methods=['GET'])
def task_status(task_id):
    # from celery.result import AsyncResult
    task_result = celery.AsyncResult(task_id)
    state = task_result.state
    result = task_result.result
    info = task_result.info

    if task_result == 'PENDING':
        response = {'state': state}
    elif task_result != 'FAILURE':
        response = {'state': state, 'result': result}
    else:
        response = {'state': state, 'error': str(info)}

    return jsonify(response)