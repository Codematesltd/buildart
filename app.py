from flask import Flask
from extensions import login_manager
from routes.admin import admin_bp
from routes.main import main_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'  # Change this in production
    
    login_manager.init_app(app)
    app.register_blueprint(main_bp)  # Register main routes at root URL
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)