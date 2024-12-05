from marshmallow import ValidationError

def validate_pdfs(files):
    if not files:
        raise ValidationError('No PDF file provided')
    
    for file in files:
        if not file.filename.endswith('.pdf'):
            raise ValidationError(f'File {file.filename} is not a PDF.')