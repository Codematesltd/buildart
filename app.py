from flask import Flask, render_template
from extensions import login_manager
from routes.admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    
    login_manager.init_app(app)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Main routes
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/about')
    def about():
        return render_template('about_us.html')
    
    @app.route('/awards')
    def awards():
        return render_template('awards.html')
    
    @app.route('/enquiry')
    def enquiry():
        return render_template('enquiry.html')
    
    @app.route('/projects')
    def projects():
        return render_template('project.html')
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)