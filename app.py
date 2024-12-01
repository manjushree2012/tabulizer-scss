from flask import Flask
from domains.file.routes.routes import file_bp

app = Flask(__name__)
app.register_blueprint(file_bp, url_prefix = '/api')

if __name__ == '__main__':
    app.run(debug=True)