from flask import Flask, render_template
from config import Config
from extensions import init_extensions, cache
from routes.admin import admin_bp
from flask_minify import minify

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    init_extensions(app)
    minify(app=app)  # Add minify initialization here
    
    # Main routes
    @app.route('/')
    @cache.cached(timeout=300)
    def index():
        return render_template('index.html')
    
    @app.route('/about')
    @cache.cached(timeout=300)
    def about():
        return render_template('about_us.html')
    
    @app.route('/awards')
    @cache.cached(timeout=300)
    def awards():
        return render_template('awards.html')
    
    @app.route('/enquiry')
    @cache.cached(timeout=300)
    def enquiry():
        return render_template('enquiry.html')
    
    @app.route('/projects')
    @cache.cached(timeout=300)
    def projects():
        return render_template('project.html')
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc')