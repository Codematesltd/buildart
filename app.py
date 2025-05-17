import os
import click
import uuid
from dotenv import load_dotenv
from flask import Flask, request
from flask_wtf.csrf import CSRFProtect, generate_csrf
from supabase import create_client
from flask_login import LoginManager
from flask_mail import Mail
from flask_minify import Minify  # Add this import
from extensions import init_extensions

# Load environment variables first
load_dotenv()

# Initialize login manager globally
login_manager = LoginManager()
mail = Mail()  # Move mail initialization here

def create_app():
    app = Flask(__name__)
    
    # Verify and initialize Supabase first
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')

    if not supabase_url or not supabase_key:
        raise ValueError("Missing Supabase credentials. Ensure SUPABASE_URL and SUPABASE_KEY are set in .env file")

    try:
        supabase = create_client(supabase_url, supabase_key)
    except Exception as e:
        raise Exception(f"Failed to initialize Supabase client: {str(e)}")
    
    # Configuration
    app.config.update(
        SECRET_KEY=os.getenv('SECRET_KEY', 'default-secret-key'),
        SUPABASE_URL=os.getenv('SUPABASE_URL'),
        SUPABASE_KEY=os.getenv('SUPABASE_KEY'),
        WTF_CSRF_ENABLED=True,
        SESSION_COOKIE_SECURE=True,         # Only send cookies over HTTPS
        SESSION_COOKIE_HTTPONLY=True,       # Prevent JavaScript access to session cookie
        SESSION_COOKIE_SAMESITE='Lax',      # Restrict cross-site cookie sending
        REMEMBER_COOKIE_SECURE=True,        # Secure remember-me cookie
        REMEMBER_COOKIE_HTTPONLY=True,      # HTTPOnly remember-me cookie
        PERMANENT_SESSION_LIFETIME=1800,    # 30 minutes session timeout
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
        MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
        MAIL_DEFAULT_SENDER=('Buildaart Careers', 'info@buildaart.com')
    )
    
    # Add Supabase client to app config
    app.config['supabase'] = supabase

    # Force HTTPS (redirect HTTP to HTTPS except in debug/local)
    @app.before_request
    def before_request_https():
        if not app.debug and not request.is_secure:
            # Allow localhost for development
            if request.host.startswith('localhost') or request.host.startswith('127.0.0.1'):
                return
            url = request.url.replace("http://", "https://", 1)
            return app.redirect(url, code=301)

    # Remove any CSP or X-Frame-Options headers (allow all external links and CDNs)
    @app.after_request
    def after_request(response):
        response.headers.pop('X-Frame-Options', None)
        response.headers.pop('Content-Security-Policy', None)
        # Set secure headers
        response.headers['Strict-Transport-Security'] = 'max-age=600; includeSubDomains; preload'
        response.headers['Referrer-Policy'] = 'no-referrer-when-downgrade'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        # Set cache headers for static files (5 minutes)
        if app.static_url_path and app.static_url_path in str(getattr(request, 'path', '')):
            # Image cache: 1 day for common image extensions
            image_exts = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.ico')
            if any(str(request.path).lower().endswith(ext) for ext in image_exts):
                response.headers['Cache-Control'] = 'public, max-age=86400'
            else:
                response.headers['Cache-Control'] = 'public, max-age=300'
        return response
    
    # Initialize CSRF protection first
    csrf = CSRFProtect()
    csrf.init_app(app)
    
    # Initialize extensions with Supabase client
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
    
    # Initialize Flask-Mail before importing routes
    mail.init_app(app)
    
    # Import routes after app and extensions are initialized
    from routes.admin import admin_bp
    from routes.main import main_bp
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Make CSRF token available to all templates
    @app.context_processor
    def inject_csrf():
        return dict(csrf_token=generate_csrf)
    
    # Provide a dummy form with csrf_token for templates if not using WTForms
    @app.context_processor
    def inject_form():
        class DummyForm:
            @property
            def csrf_token(self):
                return generate_csrf()
        return dict(form=DummyForm())
    
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