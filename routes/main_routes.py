from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/about')
def about():
    return render_template('about_us.html')

@main_bp.route('/awards')
def awards():
    return render_template('awards.html')

@main_bp.route('/enquiry')
def enquiry():
    return render_template('enquiry.html')

@main_bp.route('/projects')
def projects():
    return render_template('project.html')
