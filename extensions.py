from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

login_manager = LoginManager()
login_manager.login_view = 'admin.login'  # Specify the login route
login_manager.login_message_category = 'info'  # Optional: sets flash message category

csrf = CSRFProtect()

def init_extensions(app):
    login_manager.init_app(app)
    csrf.init_app(app)

