from flask import Flask, request, jsonify
from celery import Celery

import os
import tabula
import pandas as pd

app = Flask(__name__)

app.config['broker_url'] = 'redis://localhost:6379/0'
app.config['result_backend'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['broker_url'])
celery.conf.update(app.config)

UPLOAD_DIR = 'uploads'
PROCESSED_DIR = 'processed'

# Celery Task Definition
@celery.task(bind=True)
def long_running_task(self,filename):
    try:
        input_path = os.path.join(UPLOAD_DIR, filename)
        output_path = os.path.join(PROCESSED_DIR, f"{os.path.splitext(filename)[0]}.csv")

        print(f"Reading PDF from: {input_path}")

        
        # Extract tables from PDF
        tables = tabula.read_pdf(input_path, pages='all', multiple_tables=True)

        if not tables:  # Check if no tables were found
            raise ValueError("No tables found in the PDF.")
        
        # Combine and save tables to a single CSV
        combined_df = pd.concat(tables)
        combined_df.to_csv(output_path, index=False)
        
        return {
            'status': 'Task completed successfully!',
            'path': output_path
        }
    except Exception as exc:
        print(f"An error occurred: {exc}")  # Log the error message
        return {
            'status': 'Task failed',
            'error': str(exc)
        }

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