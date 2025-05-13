import os
import click
import uuid
from dotenv import load_dotenv
from flask import Flask
from flask_wtf.csrf import CSRFProtect, generate_csrf
from supabase import create_client
from flask_login import LoginManager

# Load environment variables first
load_dotenv()

# Initialize Supabase client
supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

from config import Config
from extensions import init_extensions
from routes.admin import admin_bp
from routes.main import main_bp
from flask_minify import Minify

# Initialize login manager globally
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config.update(
        SECRET_KEY=os.getenv('SECRET_KEY', 'default-secret-key'),
        SUPABASE_URL=os.getenv('SUPABASE_URL'),
        SUPABASE_KEY=os.getenv('SUPABASE_KEY'),
        WTF_CSRF_ENABLED=True
    )

    # Remove any CSP or X-Frame-Options headers (allow all external links and CDNs)
    @app.after_request
    def after_request(response):
        response.headers.pop('X-Frame-Options', None)
        response.headers.pop('Content-Security-Policy', None)
        return response
    
    # Initialize CSRF protection first
    csrf = CSRFProtect()
    csrf.init_app(app)
    
    # Initialize extensions
    init_extensions(app)
    
    # Initialize login manager
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        try:
            response = supabase.table('admin_users').select('*').eq('id', user_id).execute()
            if response.data:
                from routes.admin import Admin  # Import here to avoid circular import
                user_data = response.data[0]
                return Admin(user_data['id'], user_data['username'])
        except Exception as e:
            print(f"Error loading user: {e}")
        return None
    
    # Register blueprints and setup
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Make CSRF token available to all templates
    @app.context_processor
    def inject_csrf():
        return dict(csrf_token=generate_csrf)
    
    # Make supabase available to templates
    @app.context_processor
    def inject_supabase():
        return dict(supabase=supabase)

    Minify(app=app, html=True, js=False, cssless=False)

    @app.cli.command("create-admin")
    @click.argument("username")
    @click.argument("password")
    def create_admin(username, password):
        """Create a new admin user."""
        try:
            # Generate a new UUID
            user_id = str(uuid.uuid4())
            
            # Check if username already exists
            existing = supabase.table('admin_users').select('*').eq('username', username).execute()
            if existing.data:
                click.echo(f"Error: Username '{username}' already exists!")
                return

            # Insert new admin user
            user_data = {
                'id': user_id,
                'username': username,
                'password_hash': password  # In production, use proper password hashing
            }
            
            response = supabase.table('admin_users').insert(user_data).execute()
            if response.data:
                click.echo(f"Admin user '{username}' created successfully!")
            else:
                click.echo("Error creating admin user")
                
        except Exception as e:
            click.echo(f"Error: {str(e)}")

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)