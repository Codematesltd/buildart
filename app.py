from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config import Config
from extensions import login_manager
from routes.admin import admin_bp
from routes.main import main_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize CSRF protection
    csrf = CSRFProtect()
    csrf.init_app(app)
    
    # Initialize extensions
    login_manager.init_app(app)
    
    # Register blueprints
    app.register_blueprint(main_bp)  # Register main routes at root URL
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)