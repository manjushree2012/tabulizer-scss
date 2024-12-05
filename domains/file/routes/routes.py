from flask import Blueprint, request, jsonify
from setup import celery

from marshmallow import ValidationError
from .validators import validate_pdfs
from .helpers import upload_and_process_file

file_bp = Blueprint('file', __name__)

@file_bp.route('/upload', methods=['POST'])
def upload_file():
    files =  request.files.getlist("file")

    try:
        validate_pdfs(files)
    except ValidationError as err:
        response = {'status': 'error', 'message': err.messages}
        return jsonify(response), 400

    task_ids = {}
    for file in files:
        file_path, task_id = upload_and_process_file(file)
        task_ids[file.filename] = task_id
    response = {'status': 'success', 'message' : 'Queue started.', 'data' : task_ids}
    return jsonify(response), 202

@file_bp.route('/status/<task_id>', methods=['GET'])
def task_status(task_id):
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