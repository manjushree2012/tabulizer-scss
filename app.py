from flask import Flask
from domains.file.routes.routes import file_bp

app = Flask(__name__)
app.config['broker_url'] = 'redis://localhost:6379/0'
app.config['result_backend'] = 'redis://localhost:6379/0'

app.register_blueprint(file_bp, url_prefix = '/api')

UPLOAD_DIR = 'uploads'
PROCESSED_DIR = 'processed'

if __name__ == '__main__':
    app.run(debug=True)