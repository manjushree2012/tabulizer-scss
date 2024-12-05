import os
import tabula
import pandas as pd
import logging

from setup import celery

UPLOAD_DIR = '/app/uploads'

@celery.task(bind=True)
def parse_pdf(self,filename):
    try:
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
            'path': output_path,
        }
    except Exception as exc:
        log_output_path = os.path.join(UPLOAD_DIR, task_id, f"{os.path.splitext(filename)[0]}.log")

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.ERROR)
        handler = logging.FileHandler(log_output_path)
        handler.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.error(f"An error occurred in task {task_id}: {str(exc)}")

        print(f"An error occurred: {exc}")  # Log the error message
        return {
            'status': 'Task failed',
            'error': str(exc)
        }