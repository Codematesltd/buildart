from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from supabase import create_client
import os

# Setup
admin_bp = Blueprint('admin', __name__)
login_manager = LoginManager()
login_manager.login_view = 'admin.login'

# Initialize Supabase
supabase = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class Admin:
    def __init__(self, id, username):
        self.id = id
        self.username = username
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return str(self.id)

def init_extensions(app):
    login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    response = supabase.table('admin_users').select('*').eq('id', user_id).execute()
    if response.data:
        user_data = response.data[0]
        return Admin(user_data['id'], user_data['username'])
    return None

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        response = supabase.table('admin_users').select('*').eq('username', form.username.data).execute()
        if response.data and response.data[0]['password_hash'] == form.password.data:
            user_data = response.data[0]
            user = Admin(user_data['id'], user_data['username'])
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        flash('Invalid credentials')
    return render_template('admin_login.html', form=form)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin_dashboard.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

@admin_bp.route('/add_award', methods=['POST'])
@login_required
def add_award():
    if request.method == 'POST':
        award_data = {
            'year': request.form.get('year'),
            'award_name': request.form.get('award_name'),
            'project': request.form.get('project_name'),
            'prize': request.form.get('prize')
        }
        response = supabase.table('awards').insert(award_data).execute()
        if response.data:
            flash('Award added successfully!', 'success')
        return redirect(url_for('main.awards'))