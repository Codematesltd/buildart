from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman

# Initialize Flask-Login and CSRF protection
login_manager = LoginManager()
login_manager.login_view = 'admin.login'
csrf = CSRFProtect()

def init_extensions(app):
    """Initialize Flask extensions"""
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User
        try:
            response = app.config['supabase'].table('users').select('*').eq('id', user_id).execute()
            if response.data:
                return User(response.data[0])
        except Exception as e:
            print(f"Error loading user: {e}")
        return None

    csrf.init_app(app)
    # Set Flask security configs
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['REMEMBER_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['REMEMBER_COOKIE_HTTPONLY'] = True
    app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # 1 hour CSRF token expiry

    # Enforce HTTPS and set secure headers
    Talisman(app, content_security_policy=None)



