import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from routes.admin import admin_bp, init_extensions, supabase
from routes.main import main_bp
from flask_minify import Minify

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config.update(
        SECRET_KEY=os.getenv('SECRET_KEY', 'default-secret-key'),
        SUPABASE_URL=os.getenv('SUPABASE_URL'),
        SUPABASE_KEY=os.getenv('SUPABASE_KEY'),
        WTF_CSRF_ENABLED=True
    )

    # Initialize CSRF protection
    CSRFProtect(app)
    
    # Initialize extensions
    init_extensions(app)
    
    # Register blueprints and setup
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Make supabase available to templates
    @app.context_processor
    def inject_supabase():
        return dict(supabase=supabase)

    Minify(app=app, html=True, js=False, cssless=False)
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)