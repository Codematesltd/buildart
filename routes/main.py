from flask import Blueprint, render_template, request, flash, redirect, url_for
from routes.admin import supabase

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/projects')
def projects():
    return render_template('projects.html')

@main_bp.route('/awards')
def awards():
    return render_template('awards.html')

@main_bp.route('/careers')
def careers():
    return render_template('careers.html')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # Your login logic here
            return redirect(url_for('main.index'))
    return render_template('login.html', form=form)
