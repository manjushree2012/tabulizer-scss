from domains.file.routes.routes import file_bp
from setup import app

app.register_blueprint(file_bp, url_prefix = '/api')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')