from flask import Flask
from config import Config
from extensions import init_extensions
from routes.admin import admin_bp
from routes.main_routes import main_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    init_extensions(app)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)