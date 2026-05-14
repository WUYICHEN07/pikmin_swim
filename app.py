import os
from flask import Flask
from app.routes import main_bp, api_bp

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key_for_pikmin_swim')

    # 註冊 Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
