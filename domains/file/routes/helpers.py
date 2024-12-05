import os
from tasks import parse_pdf

UPLOAD_DIR = '/app/uploads'

def upload_and_process_file(file):
    task = parse_pdf.delay(file.filename)

    task_dir = os.path.join(UPLOAD_DIR, str(task.id))
    os.makedirs(task_dir, exist_ok=True)

    file_path = os.path.join(task_dir, file.filename)
    file.save(file_path)

    return file_path, task.id