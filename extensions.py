from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

login_manager = LoginManager()
<<<<<<< HEAD
login_manager.login_view = 'auth.login'  # specify the login view endpoint
login_manager.login_message_category = 'info'
=======
login_manager.login_view = 'admin.login'
csrf = CSRFProtect()

def init_extensions(app):
    login_manager.init_app(app)
    csrf.init_app(app)
>>>>>>> 018c4ac538a3de0d093ffa992b346265a128dbd5
