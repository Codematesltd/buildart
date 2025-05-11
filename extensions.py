
from flask_login import LoginManager
from flask_wtf import CSRFProtect  # Modified import
from flask_talisman import Talisman

login_manager = LoginManager()
login_manager.login_view = 'admin.login'  # Specify the login route
login_manager.login_message_category = 'info'  # Optional: sets flash message category

csrf = CSRFProtect()

def init_extensions(app):
    login_manager.init_app(app)
    csrf.init_app(app)
    # Set Flask security configs
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['REMEMBER_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['REMEMBER_COOKIE_HTTPONLY'] = True
    app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # 1 hour CSRF token expiry

    # Enforce HTTPS and set secure headers
    Talisman(app, content_security_policy=None)

