from flask import Flask
from config import Config
from extensions import init_extensions
from routes.admin import admin_bp
from routes.main import main_bp
from flask_minify import Minify

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize all extensions
    init_extensions(app)
    
    # Register blueprints
    app.register_blueprint(main_bp)  # Register main routes at root URL
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Minify HTML responses
    Minify(app=app, html=True, js=False, cssless=False)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)