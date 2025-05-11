from flask_login import LoginManager
from supabase import create_client, Client
import os

# Initialize Supabase client
supabase: Client = create_client(
    os.getenv('SUPABASE_URL', ''),
    os.getenv('SUPABASE_KEY', '')
)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'admin.login'

def init_extensions(app):
    """Initialize Flask extensions"""
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        from models.user import User
        try:
            response = supabase.table('users').select('*').eq('id', user_id).execute()
            if response.data:
                return User(response.data[0])
        except Exception as e:
            print(f"Error loading user: {e}")
        return None
