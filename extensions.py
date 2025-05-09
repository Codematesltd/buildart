from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # specify the login view endpoint
login_manager.login_message_category = 'info'
