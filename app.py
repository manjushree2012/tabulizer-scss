import os
from flask import Flask, request, jsonify
from tasks import long_running_task

app = Flask(__name__)
app.config['broker_url'] = 'redis://localhost:6379/0'
app.config['result_backend'] = 'redis://localhost:6379/0'

UPLOAD_DIR = 'uploads'
PROCESSED_DIR = 'processed'

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(file_path)

    task = long_running_task.delay(file.filename)

    response = {'state': 12, 'error': 'asas'}
    return jsonify(response, 202)

if __name__ == '__main__':
    app.run(debug=True)