import os
from flask import Blueprint, request, jsonify
from tasks import long_running_task

file_bp = Blueprint('file', __name__)

UPLOAD_DIR = 'uploads'

@file_bp.route('/upload', methods=['POST'])
def upload_file():
    files =  request.files.getlist("file")
    task_ids = {}

    for file in files:
        task = long_running_task.delay(file.filename)
        task_ids[file.filename] = task.id

        task_dir = os.path.join(UPLOAD_DIR, str(task.id))
        os.makedirs(task_dir, exist_ok=True)

        file_path = os.path.join(task_dir, file.filename)
        file.save(file_path)
    response = {'task_ids': task_ids, 'status': 'Queue started'}
    return jsonify(response), 202

@file_bp.route('/status/<task_id>', methods=['GET'])
def task_status(task_id):
    # task = long_running_task.AsyncResult(task_id)
    
    # if task.state == 'PENDING':
    #     response = {
    #         'status': 'Pending',
    #         'state': task.state
    #     }
    # elif task.state != 'FAILURE':
    #     response = {
    #         'status': 'Running' if task.state == 'PROGRESS' else 'Completed',
    #         'state': task.state,
    #         'result': task.result
    #     }
    # else:
    #     # Task failed
    #     response = {
    #         'status': 'Failed',
    #         'state': task.state,
    #         'error': str(task.result)
    #     }
    
    # return jsonify(response)

    from celery.result import AsyncResult
    task_result = AsyncResult(task_id)

    if task_result.state == 'PENDING':
        response = {'state': task_result.state}
    elif task_result.state != 'FAILURE':
        response = {'state': task_result.state, 'result': task_result.result}
    else:
        response = {'state': task_result.state, 'error': str(task_result.info)}

    return jsonify(response)