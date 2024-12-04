import os
import tabula
import pandas as pd
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379/0')

UPLOAD_DIR = 'uploads'
PROCESSED_DIR = 'processed'

@celery.task(bind=True)
def parse_pdf(self,filename):
    try:
        #Get the task ID
        task_id = self.request.id

        input_path = os.path.join(UPLOAD_DIR , task_id, filename)
        output_path = os.path.join(UPLOAD_DIR, task_id, f"{os.path.splitext(filename)[0]}.csv")

        print(f"Reading PDF from: {input_path}")

        tables = tabula.read_pdf(input_path, pages='all', multiple_tables=True)

        if not tables:
            raise ValueError("No tables found in the PDF.")
        
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