from flask import Flask
from config import Config
from extensions import init_extensions
from routes.admin import admin_bp
<<<<<<< HEAD
from routes.main import main_bp
=======
from routes.main_routes import main_bp
>>>>>>> 018c4ac538a3de0d093ffa992b346265a128dbd5

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
<<<<<<< HEAD
    login_manager.init_app(app)
    app.register_blueprint(main_bp)  # Register main routes at root URL
=======
    init_extensions(app)
    app.register_blueprint(main_bp)
>>>>>>> 018c4ac538a3de0d093ffa992b346265a128dbd5
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)