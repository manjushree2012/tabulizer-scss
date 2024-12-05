from flask import Flask
from domains.file.routes.routes import file_bp
from setup import app

# app = Flask(__name__)
# app.config['broker_url'] = 'redis://redis:6379/0'
# app.config['result_backend'] = 'redis://redis:6379/0'

app.register_blueprint(file_bp, url_prefix = '/api')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')